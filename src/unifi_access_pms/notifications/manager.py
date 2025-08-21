"""Notification manager for UniFi Access PMS."""

from typing import Dict, Any, List
from ..core.interfaces import NotificationChannel
from ..core.registry import NotificationRegistry


class NotificationManager:
    """Manages notification channels and sending."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize notification manager."""
        self.config = config
        self.channels: Dict[str, NotificationChannel] = {}
        self._initialize_channels()
    
    def _initialize_channels(self):
        """Initialize enabled notification channels."""
        notifications_config = self.config.get('notifications', {})
        enabled_channels = notifications_config.get('enabled_channels', [])
        channels_config = notifications_config.get('channels', {})
        
        for channel_name in enabled_channels:
            if channel_name in channels_config:
                channel_config = channels_config[channel_name]
                if channel_config.get('enabled', True):
                    try:
                        channel_class = NotificationRegistry.get_channel(channel_name)
                        channel = channel_class(channel_config.get('config', {}))
                        self.channels[channel_name] = channel
                    except Exception as e:
                        print(f"Failed to initialize channel {channel_name}: {e}")
    
    def send_notification(self, message: str, event_type: str = "general", **kwargs) -> bool:
        """Send notification to all enabled channels."""
        if not self.channels:
            return True  # No channels configured, consider success
        
        success = True
        for channel_name, channel in self.channels.items():
            try:
                result = channel.send_notification(message, **kwargs)
                if not result:
                    success = False
                    print(f"Failed to send notification via {channel_name}")
            except Exception as e:
                success = False
                print(f"Error sending notification via {channel_name}: {e}")
        
        return success
    
    def test_channels(self) -> Dict[str, bool]:
        """Test all configured channels."""
        results = {}
        for channel_name, channel in self.channels.items():
            try:
                result = channel.send_notification(
                    "Test notification from UniFi Access PMS",
                    title="Test Notification"
                )
                results[channel_name] = result
            except Exception as e:
                print(f"Error testing channel {channel_name}: {e}")
                results[channel_name] = False
        
        return results