# README.md


## Common Commands

- **Install dependencies**: `pip install -r requirements.txt`
- **Run the application**: `python app.py`

## Code Architecture

This is a Gradio-based chatbot application that acts as a personal AI assistant.

- **`app.py`**: The main entry point of the application. It initializes and runs the Gradio chat interface.
  - **`Me` class**: Encapsulates the core logic of the chatbot.
    - `__init__()`: Sets up the OpenAI client (configured for Google's Generative Language API), and loads personal context from `me/linkedin.pdf` and `me/summary.txt`.
    - `system_prompt()`: Creates the detailed system prompt for the AI model, instructing it to act as a specific person (`Vasu Nagpal`) using the loaded context.
    - `chat()`: Handles the user interaction logic for the Gradio interface, sending messages to the AI and processing responses.
    - `handle_tool_call()`: Manages function calls made by the AI model. Two tools are defined:
      - `record_user_details`: To capture contact information from interested users.
      - `record_unknown_question`: To log questions the AI cannot answer.
- **`me/` directory**: Contains the source data for the chatbot's persona, including a LinkedIn profile PDF and a text summary.
- **Environment Variables**: The application requires a `.env` file with the following keys for API access:
  - `GOOGLE_API_KEY`
  - `PUSHOVER_TOKEN`
  - `PUSHOVER_USER`
