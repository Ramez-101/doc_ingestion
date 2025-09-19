"""
Professional Configuration Manager
Handles application settings, user preferences, and system configuration
Version: 1.0.0
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

class ConfigManager:
    """Professional configuration management system."""
    
    DEFAULT_CONFIG = {
        "application": {
            "name": "NLP Document Processor",
            "version": "1.0.0",
            "theme": "dark",
            "auto_save": True,
            "window_geometry": "1200x800",
            "last_directory": ""
        },
        "pipeline": {
            "chunk_size": 500,
            "chunk_overlap": 50,
            "embedding_model": "all-MiniLM-L6-v2",
            "collection_name": "documents",
            "persist_dir": "./chroma_db"
        },
        "processing": {
            "max_file_size_mb": 100,
            "supported_formats": [".pdf", ".png", ".jpg", ".jpeg", ".txt"],
            "ocr_language": "eng",
            "text_extraction_timeout": 300
        },
        "ui": {
            "show_progress_details": True,
            "auto_clear_results": False,
            "max_results_display": 1000,
            "font_size": 10
        },
        "logging": {
            "level": "INFO",
            "file_logging": True,
            "max_log_size_mb": 10,
            "backup_count": 3
        }
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_dir = Path(config_dir) if config_dir else Path.home() / ".nlp_processor"
        self.config_file = self.config_dir / "config.json"
        self.log_dir = self.config_dir / "logs"
        
        # Ensure directories exist
        self.config_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)
        
        self.config = self.load_config()
        self.setup_logging()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Merge with defaults to ensure all keys exist
                merged_config = self._merge_configs(self.DEFAULT_CONFIG, config)
                return merged_config
                
            except (json.JSONDecodeError, IOError) as e:
                logging.warning(f"Failed to load config file: {e}. Using defaults.")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Save configuration to file."""
        try:
            config_to_save = config if config is not None else self.config
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
            
            logging.info("Configuration saved successfully")
            return True
            
        except IOError as e:
            logging.error(f"Failed to save configuration: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'pipeline.chunk_size')."""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> bool:
        """Set configuration value using dot notation."""
        keys = key_path.split('.')
        config_ref = self.config
        
        try:
            # Navigate to parent of target key
            for key in keys[:-1]:
                if key not in config_ref:
                    config_ref[key] = {}
                config_ref = config_ref[key]
            
            # Set the value
            config_ref[keys[-1]] = value
            
            # Auto-save if enabled
            if self.get('application.auto_save', True):
                self.save_config()
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to set config value {key_path}: {e}")
            return False
    
    def get_pipeline_config(self) -> Dict[str, Any]:
        """Get pipeline-specific configuration."""
        return self.config.get('pipeline', {})
    
    def update_pipeline_config(self, **kwargs) -> bool:
        """Update pipeline configuration."""
        try:
            pipeline_config = self.config.setdefault('pipeline', {})
            pipeline_config.update(kwargs)
            
            if self.get('application.auto_save', True):
                self.save_config()
            
            logging.info("Pipeline configuration updated")
            return True
            
        except Exception as e:
            logging.error(f"Failed to update pipeline config: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to defaults."""
        try:
            self.config = self.DEFAULT_CONFIG.copy()
            self.save_config()
            logging.info("Configuration reset to defaults")
            return True
            
        except Exception as e:
            logging.error(f"Failed to reset configuration: {e}")
            return False
    
    def setup_logging(self):
        """Setup logging based on configuration."""
        log_level = getattr(logging, self.get('logging.level', 'INFO').upper())
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[]
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logging.getLogger().addHandler(console_handler)
        
        # File handler if enabled
        if self.get('logging.file_logging', True):
            try:
                from logging.handlers import RotatingFileHandler
                
                log_file = self.log_dir / "nlp_processor.log"
                max_size = self.get('logging.max_log_size_mb', 10) * 1024 * 1024
                backup_count = self.get('logging.backup_count', 3)
                
                file_handler = RotatingFileHandler(
                    log_file,
                    maxBytes=max_size,
                    backupCount=backup_count
                )
                file_handler.setLevel(log_level)
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                file_handler.setFormatter(file_formatter)
                logging.getLogger().addHandler(file_handler)
                
            except Exception as e:
                logging.warning(f"Failed to setup file logging: {e}")
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Recursively merge user config with defaults."""
        merged = default.copy()
        
        for key, value in user.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def export_config(self, file_path: str) -> bool:
        """Export configuration to specified file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Configuration exported to {file_path}")
            return True
            
        except IOError as e:
            logging.error(f"Failed to export configuration: {e}")
            return False
    
    def import_config(self, file_path: str) -> bool:
        """Import configuration from specified file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Merge with defaults to ensure all keys exist
            self.config = self._merge_configs(self.DEFAULT_CONFIG, imported_config)
            self.save_config()
            
            logging.info(f"Configuration imported from {file_path}")
            return True
            
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Failed to import configuration: {e}")
            return False
    
    def get_config_info(self) -> Dict[str, Any]:
        """Get information about configuration."""
        return {
            "config_dir": str(self.config_dir),
            "config_file": str(self.config_file),
            "log_dir": str(self.log_dir),
            "config_exists": self.config_file.exists(),
            "config_size": self.config_file.stat().st_size if self.config_file.exists() else 0,
            "last_modified": self.config_file.stat().st_mtime if self.config_file.exists() else None
        }

# Global configuration instance
_config_manager = None

def get_config_manager() -> ConfigManager:
    """Get global configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

def get_config(key_path: str, default: Any = None) -> Any:
    """Convenience function to get configuration value."""
    return get_config_manager().get(key_path, default)

def set_config(key_path: str, value: Any) -> bool:
    """Convenience function to set configuration value."""
    return get_config_manager().set(key_path, value)
