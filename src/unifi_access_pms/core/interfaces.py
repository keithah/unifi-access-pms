"""Core interfaces for UniFi Access PMS."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

from .models import Reservation, Visitor


class ReservationProvider(ABC):
    """Abstract base class for reservation providers."""
    
    @abstractmethod
    def get_reservations(self, start_date: datetime, end_date: datetime) -> List[Reservation]:
        """Fetch reservations for the given date range."""
        pass
    
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate provider configuration."""
        pass


class NotificationChannel(ABC):
    """Abstract base class for notification channels."""
    
    @abstractmethod
    def send_notification(self, message: str, **kwargs) -> bool:
        """Send a notification message."""
        pass
    
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate channel configuration."""
        pass


class UniFiAccessIntegration(ABC):
    """Abstract base class for UniFi Access integration."""
    
    @abstractmethod
    def get_visitors(self) -> List[Visitor]:
        """Get all current visitors."""
        pass
    
    @abstractmethod
    def create_visitor(self, visitor: Visitor) -> str:
        """Create a new visitor and return the visitor ID."""
        pass
    
    @abstractmethod
    def update_visitor(self, visitor_id: str, visitor: Visitor) -> bool:
        """Update an existing visitor."""
        pass
    
    @abstractmethod
    def delete_visitor(self, visitor_id: str) -> bool:
        """Delete a visitor."""
        pass