"""Logging utility for the application."""

import logging
import os
from datetime import datetime
from typing import Optional

# ANSI color codes
COLORS = {
    'DEBUG': '\033[36m',    # Cyan
    'INFO': '\033[32m',     # Green
    'WARNING': '\033[33m',  # Yellow
    'ERROR': '\033[31m',    # Red
    'CRITICAL': '\033[35m', # Magenta
    'RESET': '\033[0m'      # Reset
}

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output."""
    
    def format(self, record):
        # Add color to the level name
        levelname = record.levelname
        if levelname in COLORS:
            record.levelname = f"{COLORS[levelname]}{levelname}{COLORS['RESET']}"
        return super().format(record)

def setup_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """Set up a logger with both console and file output.
    
    Args:
        name: The name of the logger
        log_file: Optional specific log file name
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Generate log filename if not provided
    if log_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f"logs/{name}_{timestamp}.log"
    else:
        log_file = f"logs/{log_file}"
    
    # File handler with detailed formatting
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler with colored output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create default loggers
app_logger = setup_logger('app')
scraper_logger = setup_logger('scraper')

# Create a logger
ai_logger = logging.getLogger('ai_logger')
ai_logger.setLevel(logging.INFO)

# Create a file handler
log_file_path = os.path.join(os.path.dirname(__file__), 'ai_analysis.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
ai_logger.addHandler(file_handler)
ai_logger.addHandler(console_handler)