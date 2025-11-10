"""
Logging System
Centralized logging configuration
"""

import logging
import os
from typing import Optional
from config_manager import ConfigManager


def setup_logger(name: str, log_file: Optional[str] = None, level: Optional[str] = None) -> logging.Logger:
    """
    Set up and return a logger with console and file handlers.
    
    Args:
        name: Logger name
        log_file: Path to log file (optional)
        level: Logging level (optional)
    
    Returns:
        Configured logger instance
    """
    config = ConfigManager()
    
    # Get configuration
    if log_file is None:
        log_file = config.get('logging.file', 'edge_detection.log')
    if level is None:
        level = config.get('logging.level', 'INFO')
    log_format = config.get('logging.format', 
                           '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create formatters
    formatter = logging.Formatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else '.', exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Create default logger
default_logger = setup_logger('edge_detection')
