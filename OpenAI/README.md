# Resume Bots with OpenAI

This repository contains two implementations of a conversational AI chatbot designed to answer questions based on a personal resume. Both bots leverage OpenAI's models and are presented with a Gradio web interface, but they showcase different methods for integrating with the OpenAI API.

## Projects

### 1. ResumeBotUsingOpenAIAgentSDK

This project demonstrates how to build the resume bot using the `openai-agents` SDK, which provides a higher-level abstraction for creating and managing AI agents.

**Key Features:**
- **Agent-Based Architecture:** Utilizes the `Agent` and `Runner` classes from the `openai-agents` library.
- **Simplified Tool Creation:** Uses the `@function_tool` decorator to easily convert Python functions into tools the agent can use.
- **Context-Aware:** Reads from a PDF resume and a summary text file to build its knowledge base.
- **Interactive UI:** A simple and clean chat interface powered by Gradio.

**Setup and Usage:**

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd ResumeBotUsingOpenAIAgentSDK
    ```

3.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure your environment:**
    Create a `.env` file in the project root and add your API keys:
    ```
    OPENAI_API_KEY="sk-..."
    PUSHOVER_TOKEN="..."
    PUSHOVER_USER="..."
    ```

6.  **Add your resume files:**
    Place your `linkedin.pdf` and `summary.txt` files inside the `me` directory.

7.  **Run the application:**
    ```bash
    python app.py
    ```

### 2. ResumeBotUsingOpenAILib

This project builds the same resume bot using the standard `openai` Python library, demonstrating how to handle tool calls manually.

**Key Features:**
- **Core OpenAI Library:** Interacts directly with the OpenAI Chat Completions API.
- **Manual Tool Handling:** Manually defines the JSON schema for tools and processes `tool_calls` from the API response.
- **Context-Aware:** Reads from a PDF resume and a summary text file, similar to the Agent SDK version.
- **Interactive UI:** A simple and clean chat interface powered by Gradio.

**Setup and Usage:**

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd ResumeBotUsingOpenAILib
    ```

3.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure your environment:**
    Create a `.env` file in the project root and add your API keys:
    ```
    OPENAI_API_KEY="sk-..."
    PUSHOVER_TOKEN="..."
    PUSHOVER_USER="..."
    ```

6.  **Add your resume files:**
    Place your `linkedin.pdf` and `summary.txt` files inside the `me` directory.

7.  **Run the application:**
    ```bash
    python app.py
    ```

## Key Differences

- **Abstraction Level:** The `Agent SDK` version offers a higher-level, more abstracted approach, simplifying agent creation and tool integration. The `OpenAI Library` version provides more granular control but requires manual handling of the tool-calling loop.
- **Tool Definition:** The SDK uses a simple decorator (`@function_tool`) to create tools, while the library version requires you to define the tool's JSON schema explicitly.
- **Dependencies:** While the `requirements.txt` are similar, the core logic in the `Agent SDK` version relies on the `openai-agents` package, whereas the other version uses the base `openai` package.
