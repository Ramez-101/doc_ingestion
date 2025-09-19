"""
Configuration module for NLP Document Processor
Contains configuration management and settings
"""

from .config_manager import ConfigManager, get_config_manager, get_config, set_config

__all__ = [
    'ConfigManager',
    'get_config_manager',
    'get_config',
    'set_config'
]
