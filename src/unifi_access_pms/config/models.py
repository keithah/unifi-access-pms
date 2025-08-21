"""Configuration models for UniFi Access PMS."""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class CoreConfig:
    """Core configuration settings."""
    enabled_providers: List[str] = field(default_factory=list)
    pin_generation_method: str = "phone_based"
    timezone: str = "UTC"
    sync_interval: Optional[int] = None


@dataclass
class UniFiConfig:
    """UniFi Access configuration."""
    api_host: str = ""
    api_token: str = ""


@dataclass
class ProviderConfig:
    """Provider configuration."""
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)
    priority: int = 1
    retry_attempts: int = 3


@dataclass
class NotificationChannelConfig:
    """Notification channel configuration."""
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NotificationConfig:
    """Notification configuration."""
    enabled_channels: List[str] = field(default_factory=list)
    channels: Dict[str, NotificationChannelConfig] = field(default_factory=dict)
    events: List[str] = field(default_factory=lambda: ["sync_complete", "error"])


@dataclass
class Config:
    """Main configuration class."""
    core: Optional[CoreConfig] = None
    unifi: Optional[UniFiConfig] = None
    providers: Optional[Dict[str, ProviderConfig]] = None
    notifications: Optional[NotificationConfig] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create Config from dictionary."""
        config = cls()
        
        if 'core' in data:
            config.core = CoreConfig(**data['core'])
        
        if 'unifi' in data:
            config.unifi = UniFiConfig(**data['unifi'])
        
        if 'providers' in data:
            providers = {}
            for name, provider_data in data['providers'].items():
                providers[name] = ProviderConfig(**provider_data)
            config.providers = providers
        
        if 'notifications' in data:
            notif_data = data['notifications']
            channels = {}
            if 'channels' in notif_data:
                for name, channel_data in notif_data['channels'].items():
                    channels[name] = NotificationChannelConfig(**channel_data)
            
            config.notifications = NotificationConfig(
                enabled_channels=notif_data.get('enabled_channels', []),
                channels=channels,
                events=notif_data.get('events', ["sync_complete", "error"])
            )
        
        return config
    
    def validate(self) -> bool:
        """Validate configuration."""
        if not self.core:
            raise ValueError("Core configuration is required")
        
        if not self.unifi:
            raise ValueError("UniFi configuration is required")
        
        if not self.unifi.api_host:
            raise ValueError("UniFi API host is required")
        
        if not self.unifi.api_token:
            raise ValueError("UniFi API token is required")
        
        return True