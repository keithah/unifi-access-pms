"""Registry for providers and notification channels."""

from typing import Dict, Type, List
from ..core.interfaces import ReservationProvider, NotificationChannel


class ProviderRegistry:
    """Registry for reservation providers."""
    
    _providers: Dict[str, Type[ReservationProvider]] = {}
    
    @classmethod
    def register(cls, name: str, provider_class: Type[ReservationProvider]):
        """Register a provider."""
        cls._providers[name] = provider_class
    
    @classmethod
    def get_provider(cls, name: str) -> Type[ReservationProvider]:
        """Get a provider by name."""
        if name not in cls._providers:
            raise ValueError(f"Unknown provider: {name}")
        return cls._providers[name]
    
    @classmethod
    def list_providers(cls) -> List[str]:
        """List all registered providers."""
        return list(cls._providers.keys())


class NotificationRegistry:
    """Registry for notification channels."""
    
    _channels: Dict[str, Type[NotificationChannel]] = {}
    
    @classmethod
    def register(cls, name: str, channel_class: Type[NotificationChannel]):
        """Register a notification channel."""
        cls._channels[name] = channel_class
    
    @classmethod
    def get_channel(cls, name: str) -> Type[NotificationChannel]:
        """Get a channel by name."""
        if name not in cls._channels:
            raise ValueError(f"Unknown notification channel: {name}")
        return cls._channels[name]
    
    @classmethod
    def list_channels(cls) -> List[str]:
        """List all registered channels."""
        return list(cls._channels.keys())


# Register built-in providers and channels
def register_builtin_providers():
    """Register built-in providers."""
    try:
        from ..providers.hospitable import HospitableProvider
        ProviderRegistry.register('hospitable', HospitableProvider)
    except ImportError:
        pass


def register_builtin_channels():
    """Register built-in notification channels."""
    try:
        from ..notifications.simplepush import SimplepushChannel
        NotificationRegistry.register('simplepush', SimplepushChannel)
    except ImportError:
        pass
    
    try:
        from ..notifications.matrix import MatrixChannel
        NotificationRegistry.register('matrix', MatrixChannel)
    except ImportError:
        pass


# Auto-register built-ins
register_builtin_providers()
register_builtin_channels()