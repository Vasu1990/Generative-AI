import gradio as gr
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import chromadb
import os
import tool
from langchain_community.vectorstores import Chroma
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import Optional
import requests

load_dotenv()

# Global configs
name = "Vasu Nagpal"
collection_name = "my_vector_store_new"
chunk_size = 1000
chunk_overlap = 200
chunks_to_search = 1

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )

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

    emb = OpenAIEmbeddings(model="text-embedding-3-large")

    vectorstore = Chroma.from_documents(
        client=chroma_client,
        documents=chunks,
    embedding=emb,
    collection_name=collection_name
)

print(vectorstore._collection.count())
retriever = vectorstore.as_retriever(search_kwargs={"k": chunks_to_search})
print("Vectorstore created and retriever ready.", retriever)

llm = ChatOpenAI(model="gpt-4o")
system_prompt = f"""
You are {name}. You are answering questions as {name}, \
particularly questions related to {name}'s career, background, skills and experience. \
Use the documents provided as context as the source of truth to answer any question. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
Answer the user's question based on the context below:

<context>
{{context}}
</context>
"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# create_stuff_documents_chain will replace the document in the context variable
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(retriever, question_answer_chain)


# Function Gradio calls for each message
def chat_fn(user_input, history):
    chat_history = []
    for human, ai in history:
        chat_history.append(HumanMessage(content=human))
        chat_history.append(AIMessage(content=ai))

    result = rag_chain.invoke({
        "input": user_input,
        "chat_history": chat_history
    })

    return result["answer"]

# Build Gradio interface
demo = gr.ChatInterface(fn=chat_fn,
    title="OpenAI RAG Chatbot",
    description=f"Ask questions about {name}."
).launch()
