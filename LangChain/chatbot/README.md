# LangChain Chatbot with RAG and Gradio

This repository contains a collection of Python scripts and a Jupyter notebook that demonstrate how to build a Retrieval-Augmented Generation (RAG) chatbot using LangChain, OpenAI, ChromaDB, and Gradio.

## Features

- **Document Ingestion**: The chatbot can load documents (PDFs and TXT files) from a local directory (`me/`), split them into chunks, and store them as embeddings in a ChromaDB vector store.
- **Retrieval-Augmented Generation (RAG)**: The chatbot uses a retrieval chain to find relevant document snippets from the vector store to answer user questions.
- **Conversation History**: One version of the chatbot (`app_history_aware.py`) is capable of retaining conversation history to answer follow-up questions.
- **Tool Usage**: The main application (`app.py`) demonstrates how to equip the chatbot with tools, such as searching the vector store and recording user details.
- **Web Interface**: A user-friendly chat interface is provided using Gradio.
- **Multiple Implementations**: The repository includes several Python scripts (`app.py`, `app_history_aware.py`, `app_using_chian.py`) that showcase different ways to build the chatbot, from a simple RAG implementation to a more advanced agent-based approach with tools.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r chatbot/requirements.txt
    ```

4.  **Create a `.env` file:**
    In the root of the `chatbot` directory, create a file named `.env` and add your OpenAI API key:
    ```
    OPENAI_API_KEY="your-openai-api-key"
    ```
    If you want to use the push notification feature in `app.py`, also add your Pushover credentials:
    ```
    PUSHOVER_TOKEN="your-pushover-app-token"
    PUSHOVER_USER="your-pushover-user-key"
    ```

5.  **Add your documents:**
    Place your personal documents (e.g., resume, profile information in `.pdf` or `.txt` format) inside the `chatbot/me/` directory. The application will load these files into the vector store on its first run.

## How to Use

You can run any of the provided chatbot applications.

-   **For the agent-based chatbot with tools:**
    ```bash
    python chatbot/app.py
    ```

-   **For the history-aware chatbot:**
    ```bash
    python chatbot/app_history_aware.py
    ```

-   **For a simpler RAG chatbot:**
    ```bash
    python chatbot/app_using_chian.py
    ```

After running one of the scripts, a local Gradio URL will be printed to the console (e.g., `http://127.0.0.1:7860`). Open this URL in your web browser to interact with the chatbot.

## Files in this Repository

-   `chatbot/app.py`: The main application featuring a LangChain agent with tools for document search and user detail recording.
-   `chatbot/app_history_aware.py`: A chatbot that can remember previous parts of the conversation.
-   `chatbot/app_using_chian.py`: A more straightforward implementation of a RAG chatbot.
-   `chatbot/chatbot.ipynb`: A Jupyter notebook for experimenting with the chatbot's components.
-   `chatbot/requirements.txt`: A list of Python dependencies for the project.
-   `chatbot/me/`: A directory to store your personal documents for the chatbot to learn from.
-   `chatbot/chroma_db/`: The directory where the ChromaDB vector store is persisted.
