# Competitor Research Tool

A Streamlit application that performs competitive analysis by searching and comparing products across multiple e-commerce websites. It leverages AI-powered insights using Google's Gemini models to provide a comprehensive understanding of the competitive landscape.

## Features

- **Multi-Store Search:** Simultaneously search for products across a wide range of stores.
- **Product Comparison:** Compare total product counts and available filters (facets) between stores.
- **AI-Powered Analysis:** Get in-depth competitive insights, including key findings, detailed analysis, and actionable recommendations.
- **Flexible AI Configuration:** Choose between a single, comprehensive AI prompt or multiple, targeted prompts for analysis.
- **Downloadable Reports:** Download the complete AI analysis as a Markdown file.
- **Debug Mode:** View raw API responses for troubleshooting and development.

## Supported Stores

- Academy Sports
- Amazon
- Dick's Sporting Goods
- Home Depot
- Lowe's
- Tractor Supply
- Walmart

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd competitor-research-tool
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file** in the root directory and add the following configuration:
    ```env
    # Google Gemini API Key
    GOOGLE_API_KEY="your_gemini_api_key_here"

    # AI Model Configuration
    GEMINI_MODEL_NAME="gemini-1.5-pro"
    MAX_OUTPUT_TOKENS=2048
    TEMPERATURE=0.7

    # Set to true to use a single prompt for analysis, false for multiple prompts
    USE_SINGLE_PROMPT=true

    # Rate Limiting for AI model
    MAX_REQUESTS_PER_MINUTE=60
    ```

## How to Run

1.  **Start the Streamlit application:**
    ```bash
    streamlit run main.py
    ```

2.  Open your browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## Project Structure

-   `main.py`: The main Streamlit application.
-   `scrapers/`: Contains the scraping logic for each supported store.
-   `processors/`: Contains the data processing logic for each store's scraped data.
-   `utils/`: Utility modules for AI analysis, logging, and more.
-   `config/`: Configuration files for AI models, stores, and categories.
-   `prompts/`: Markdown templates for the AI prompts.
-   `requirements.txt`: A list of all the Python dependencies.

## AI Features

The application uses Google's Gemini models to provide:

-   **Key Findings:** A high-level summary of the competitive landscape.
-   **Detailed Analysis:** An in-depth comparison of product offerings and filter structures.
-   **Recommendations:** Actionable insights and suggestions based on the analysis.

## Configuration

-   **AI Model:** Adjust AI model parameters in the `.env` file.
-   **Prompt Templates:** Modify the AI prompt templates in the `prompts/` directory.
-   **Caching and Rate Limiting:** Configure caching and rate limiting in `config/ai_config.py`.
-   **Stores and Categories:** Manage the list of supported stores and category mappings in `config/all-stores.json` and `config/category-vendor.json`.
