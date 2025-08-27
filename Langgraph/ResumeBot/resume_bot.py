from typing import Annotated
import chromadb
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from IPython.display import Image, display
import gradio as gr
from langgraph.prebuilt import ToolNode, tools_condition
import requests
import os
from langchain_openai import ChatOpenAI
from typing import TypedDict
from langchain.agents import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.vectorstores import Chroma
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import datetime

load_dotenv(override=True)

name="Vasu Nagpal"
pushover_token = os.getenv("PUSHOVER_TOKEN")
collection_name = "my_vector_store_langgraph"
chunk_size = 512
chunk_overlap = 50
chunks_to_search = 5

pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"


# Initialize raw Chroma client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# List existing collections
existing_collections = chroma_client.list_collections()
print("Existing collections:", existing_collections)


#check if collection exists do not create again
if collection_name in existing_collections:
    vectorstore = Chroma.from_existing_collection(collection_name)
else:
    # 1️⃣ Path to "me" folder (parallel to the script file)
    me_folder = Path(__file__).resolve().parent / "me"
 
    # 2️⃣ Load all TXT files
    txt_loader = DirectoryLoader(
        path=str(me_folder),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"autodetect_encoding": True},
    )

    # 3️⃣ Load all PDF files
    pdf_loader = DirectoryLoader(
        path=str(me_folder),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
    )
    # 4️⃣ Load documents
    docs = pdf_loader.load()
    print(f"Loaded {len(docs)} documents from 'me' folder")

    # 5️⃣ Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = text_splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks in total")
    print(chunks[0].page_content[:1000])  # preview first chunk

    emb = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = Chroma.from_documents(
        client=chroma_client,
        documents=chunks,
    embedding=emb,
    collection_name=collection_name
)

print(vectorstore._collection.count())
retriever = vectorstore.as_retriever(
    search_type="similarity",  # Maximal Marginal Relevance: more diverse, less redundant
    search_kwargs={"k": chunks_to_search}  # fetch more, return best 8
)
print("Vectorstore created and retriever ready.", retriever)

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

def push(text: str):
    """Send a push notification to the user"""
    requests.post(pushover_url, data = {"token": pushover_token, "user": pushover_user, "message": text})

def doc_search(query: str):
    """Searches your vectorstore for relevant documents.
    Always use this tool to answer questions about resume.
    Returns numbered snippets that MUST be cited."""
    docs = retriever.get_relevant_documents(query)
    if not docs:
        return "NO_SOURCES"

    print(docs)

    results = []
    for i, doc in enumerate(docs, 1):
        snippet = doc.page_content.replace("\n", " ")
        results.append(f"[{i}] {snippet}")  # cap length
    return results


tool_push = Tool(
        name="send_push_notification",
        func=push,
        description="useful for when you want to send a push notification"
    )

tools = [tool_push]
# Step 1: Create a State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Step 2: Create a State Graph
graph_builder = StateGraph(State)

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

system_prompt = f"""
You are {name}, answering as {name}'s professional assistant.
- Use the provided context to answer any question related to {name}'s career, skills, or background.
- Try creating your response based on the data or infer answer from it based on your understanding.
- If you cannot find an answer, politely say you could not find that in the resume and send a push notification using the tools.
- If a user shares their email or wants to connect, record it with the `record_user_details` tool.
- If a user is interested to connect send me a push notification using the available tools.

Context:
{{context}}

"""



# Step 3: Create a Node
def chatbot(state: State):
    print(state["messages"])
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))

# Step 4: Create Edges
graph_builder.add_conditional_edges( "chatbot", tools_condition, "tools")

# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

# Step 5: Compile the Graph
graph = graph_builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))


def chat(user_input: str, history):
    doc_search_results = doc_search(user_input)
    context = doc_search_results if doc_search_results != "NO_SOURCES" else ""
    prompt = system_prompt.format(context=context)
    messages = [{"role": "system", "content": prompt}]
    messages += [{"role": "user", "content": user_input}]
    result = graph.invoke({"messages": messages})
    return result["messages"][-1].content


gr.ChatInterface(chat, type="messages").launch()