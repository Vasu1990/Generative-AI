"""Configuration for AI models and settings."""

import os
from dotenv import load_dotenv
from typing import Dict

# Load environment variables
load_dotenv()

# Model-specific configurations
MODEL_CONFIGS: Dict[str, Dict] = {
    "gemini-1.5-pro": {
        "max_input_tokens": 30720,   # Actual limit for Gemini 1.5 Pro
        "max_output_tokens": 2048,   # Conservative default
        "supports_streaming": True
    },
    "gemini-2.0-flash-thinking-exp-01-21": {
        "max_input_tokens": 30720,   # Using same as 1.5 Pro until official specs
        "max_output_tokens": 2048,   # Conservative default
        "supports_streaming": True
    }
}

def get_model_config(model_name: str) -> Dict:
    """Get configuration for specified model with fallback defaults."""
    default_config = {
        "max_input_tokens": 30720,  # Conservative default
        "max_output_tokens": 2048,  # Conservative default
        "supports_streaming": True
    }
    return MODEL_CONFIGS.get(model_name, default_config)

# Get model name from environment
model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-pro")
model_config = get_model_config(model_name)

# Gemini Configuration
GEMINI_CONFIG = {
    "api_key": os.getenv("GOOGLE_API_KEY"),
    "model_name": model_name,
    "max_input_tokens": model_config["max_input_tokens"],
    "max_output_tokens": model_config["max_output_tokens"],
    "temperature": float(os.getenv("TEMPERATURE", "0.7")),
    "rate_limit": int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60")),
    "supports_streaming": model_config["supports_streaming"]
}

# Prompt Templates Directory
PROMPT_TEMPLATES_DIR = "prompts"

# Cache Configuration
CACHE_CONFIG = {
    "cache_dir": ".cache",
    "max_cache_size": 100,  # Number of responses to cache
    "cache_ttl": 3600  # Cache time-to-live in seconds
}

# Error Messages
ERROR_MESSAGES = {
    "api_key_missing": "Gemini API key not found. Please set GOOGLE_API_KEY in .env file.",
    "rate_limit_exceeded": "API rate limit exceeded. Please try again later.",
    "model_error": "Error generating insights. Please try again.",
    "invalid_response": "Invalid response from AI model. Please try again.",
    "token_limit_exceeded": "Input exceeds model's token limit. Please reduce the input size."
} 