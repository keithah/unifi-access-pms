"""Matrix notification channel."""

import requests
import json
from typing import Dict, Any

from ..core.interfaces import NotificationChannel


class MatrixChannel(NotificationChannel):
    """Matrix notification channel."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Matrix channel."""
        self.config = config
        self.homeserver = config.get('homeserver')
        self.access_token = config.get('access_token')
        self.room_id = config.get('room_id')
        
        if not all([self.homeserver, self.access_token, self.room_id]):
            raise ValueError("Matrix homeserver, access_token, and room_id are required")
        
        # Ensure homeserver has proper format
        if not self.homeserver.startswith('http'):
            self.homeserver = f"https://{self.homeserver}"
    
    def send_notification(self, message: str, **kwargs) -> bool:
        """Send notification via Matrix."""
        try:
            title = kwargs.get('title', 'UniFi Access PMS')
            
            # Matrix API endpoint
            url = f"{self.homeserver}/_matrix/client/r0/rooms/{self.room_id}/send/m.room.message"
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            # Message payload with rich formatting
            payload = {
                'msgtype': 'm.text',
                'body': f"{title}\n\n{message}",  # Plain text fallback
                'format': 'org.matrix.custom.html',
                'formatted_body': f"<b>{title}</b><br><br>{message.replace(chr(10), '<br>')}"
            }
            
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(payload),
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"📱 Matrix notification sent to room {self.room_id}")
                return True
            else:
                print(f"⚠️ Matrix notification failed: {response.status_code} - {response.text}")
                return False
            
        except Exception as e:
            print(f"Failed to send Matrix notification: {e}")
            return False
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate Matrix configuration."""
        required_fields = ['homeserver', 'access_token', 'room_id']
        return all(field in config for field in required_fields)