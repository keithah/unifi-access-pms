"""Configuration manager for UniFi Access PMS."""

import yaml
from pathlib import Path
from typing import Dict, Any

from .models import Config


class ConfigManager:
    """Manages configuration loading and validation."""
    
    def __init__(self, config_path: str):
        """Initialize configuration manager."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Config:
        """Load configuration from file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        return Config.from_dict(config_data)
    
    def validate(self) -> bool:
        """Validate the loaded configuration."""
        return self.config.validate()
    
    def get_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """Get configuration for a specific provider."""
        providers = self.config.providers or {}
        return providers.get(provider_name, {}).get('config', {})
    
    def get_notification_config(self, channel_name: str) -> Dict[str, Any]:
        """Get configuration for a specific notification channel."""
        notifications = self.config.notifications or {}
        channels = notifications.get('channels', {})
        return channels.get(channel_name, {}).get('config', {})