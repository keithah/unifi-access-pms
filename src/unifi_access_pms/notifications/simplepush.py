"""Simplepush notification channel."""

import requests
from typing import Dict, Any

from ..core.interfaces import NotificationChannel


class SimplepushChannel(NotificationChannel):
    """Simplepush notification channel."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Simplepush channel."""
        self.config = config
        self.key = config.get('key')
        if not self.key:
            raise ValueError("Simplepush key is required")
    
    def send_notification(self, message: str, **kwargs) -> bool:
        """Send notification via Simplepush."""
        try:
            title = kwargs.get('title', 'UniFi Access PMS')
            
            response = requests.post(
                'https://api.simplepush.io/send',
                data={
                    'key': self.key,
                    'title': title,
                    'msg': message
                },
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Failed to send Simplepush notification: {e}")
            return False
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate Simplepush configuration."""
        return 'key' in config and config['key']