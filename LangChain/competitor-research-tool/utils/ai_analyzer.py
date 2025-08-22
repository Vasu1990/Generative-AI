"""AI analysis module using Google's Gemini API."""

import os
import json
from pathlib import Path
import google.generativeai as genai
from config.ai_config import GEMINI_CONFIG
from utils.logger import ai_logger

def init_gemini():
    """Initialize Gemini API client."""
    try:
        genai.configure(api_key=GEMINI_CONFIG["api_key"])
        model = genai.GenerativeModel(
            model_name=GEMINI_CONFIG["model_name"],
            generation_config={
                "temperature": GEMINI_CONFIG["temperature"],
                "max_output_tokens": GEMINI_CONFIG["max_output_tokens"],
            }
        )
        return model
    except Exception as e:
        ai_logger.error(f"Failed to initialize Gemini: {str(e)}")
        raise

def load_prompt_template(store_name, section="competitive_analysis"):
    """Load the competitive analysis prompt template."""
    try:
        # prompt_path = Path("prompts/competitive_analysis.md")
        prompt_path = Path(f"prompts/{section}.md")
        with open(prompt_path, 'r', encoding='utf-8') as f:
            template = f.read()
        # Replace the placeholder with the actual store name
        template = template.replace("<Store>", store_name)
        return template
    except Exception as e:
        ai_logger.error(f"Failed to load prompt template: {str(e)}")
        raise

def generate_analysis(data, search_term, store_name, section="competitive_analysis"):
    """Generate competitive analysis using Gemini.
    
    Args:
        data: Combined facet data from both stores
        search_term: The search term used
        
    Returns:
        dict: Structured analysis results
    """
    try:
        # Initialize Gemini
        model = init_gemini()

        # Check if using single prompt or multiple prompts
        use_single_prompt = os.getenv('USE_SINGLE_PROMPT', 'true').lower() == 'true'

        if use_single_prompt:
            # Load single prompt template
            template = load_prompt_template(store_name=store_name, section='competitive_analysis')
            prompt = template + f"\n\nSearch Term: {search_term}\nData: {json.dumps(data, indent=2)}"
            ai_logger.info(f"Sending single prompt for analysis of {search_term}")
        else:
            # Load section-specific prompt template
            template = load_prompt_template(store_name=store_name, section=section)
            prompt = template + f"\n\nSearch Term: {search_term}\nData: {json.dumps(data, indent=2)}"
            ai_logger.info(f"Sending {section} prompt for analysis of {search_term}")

        # Log the prompt
        ai_logger.info(f"Prompt sent to LLM: {prompt}")

        # Generate analysis
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            raise ValueError("Empty response from Gemini")

        ai_logger.info(f"Received response for {section if section else 'full analysis'}: {response.text}")

        ai_logger.info("Successfully generated analysis")
        return response.text.encode('utf-8').decode('utf-8')
        
    except Exception as e:
        ai_logger.error(f"Failed to generate {section if section else 'full analysis'}: {str(e)}")
        raise