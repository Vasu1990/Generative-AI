import gradio as gr
from dotenv import load_dotenv
import chromadb
import os
from pathlib import Path
import datetime
import requests


from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import Optional
from langchain_core.tools import tool
from langchain.chat_models import ChatOpenAI
from langchain.agents import tool, create_openai_functions_agent, AgentExecutor


load_dotenv()

# Global configs
name = "Vasu Nagpal"
collection_name = "my_vector_store_new1"
chunk_size = 512
chunk_overlap = 50
chunks_to_search = 5

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )

# #set below function as langchain tool
@tool
def record_user_details(email: str, name: Optional[str] = None, notes: Optional[str] = None) -> dict:
    """Record user details when they provide an email for follow-up contact.

    Args:
        email (str): The user's email address for follow-up.
        name (str, optional): The user's name. Defaults to None.
        notes (str, optional): Additional notes about the user. Defaults to None.
    """
    name = name or "Name not provided"
    notes = notes or "not provided"
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

@tool
def doc_search(query: str):
    """Searches your vectorstore for relevant documents.
    Always use this tool to answer questions about resume.
    Returns numbered snippets that MUST be cited."""
    docs = retriever.get_relevant_documents(query)
    if not docs:
        return "NO_SOURCES"

    results = []
    for i, doc in enumerate(docs, 1):
        snippet = doc.page_content.replace("\n", " ")
        results.append(f"[{i}] {snippet[:500]}")  # cap length
    return "\n".join(results)


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
    docs = txt_loader.load() + pdf_loader.load()
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

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
system_prompt = f"""
You are {name}, answering as {name}'s professional assistant.
STRICT RULES:
- You MUST call the `doc_search` tool before answering questions about {name}'s career, skills, or background.
- Only use information from the tool output. Do NOT make up answers.
- Always cite snippets like [1], [2].
- If `doc_search` returns "NO_SOURCES", politely say you could not find that in the resume,
  and send a push notification using the tools.
- If a user shares their email or wants to connect, record it with the `record_user_details` tool.
If a user is interested to connect send me a push notification using the available tools.
Today's date is {current_date}.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

tools = [record_user_details, doc_search]
agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)


# Function Gradio calls for each message
def chat_fn(user_input, history):
    chat_history = []
    for human, ai in history:
        chat_history.append(HumanMessage(content=human))
        chat_history.append(AIMessage(content=ai))

    result = executor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })

    return result["output"] 

# Build Gradio interface
demo = gr.ChatInterface(fn=chat_fn,
    title="OpenAI RAG Chatbot",
    description=f"Ask questions about {name}."
).launch()
