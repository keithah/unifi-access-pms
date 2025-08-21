"""Core data models for UniFi Access PMS."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Guest:
    """Guest information."""
    first_name: str
    last_name: str
    phone: Optional[str] = None
    email: Optional[str] = None


@dataclass
class Reservation:
    """Reservation data model."""
    id: str
    guest: Guest
    check_in: datetime
    check_out: datetime
    status: str
    property_id: str
    property_name: Optional[str] = None
    
    @property
    def guest_name(self) -> str:
        """Get full guest name."""
        return f"{self.guest.first_name} {self.guest.last_name}"


@dataclass
class Visitor:
    """UniFi Access visitor data model."""
    id: Optional[str] = None
    name: str = ""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    pin: str = ""
    status: str = "active"
    
    def __post_init__(self):
        """Validate visitor data after initialization."""
        if not self.name:
            raise ValueError("Visitor name is required")
        if len(self.pin) < 4:
            raise ValueError("PIN must be at least 4 digits")


@dataclass
class SyncResult:
    """Result of a synchronization operation."""
    total_processed: int = 0
    created: int = 0
    updated: int = 0
    deleted: int = 0
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as a percentage."""
        if self.total_processed == 0:
            return 100.0
        failed = len(self.errors)
        return ((self.total_processed - failed) / self.total_processed) * 100