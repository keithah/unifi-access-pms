"""Test core functionality."""

import pytest
from datetime import datetime

from src.unifi_access_pms.core.models import Guest, Reservation, Visitor


def test_guest_creation():
    """Test guest model creation."""
    guest = Guest(
        first_name="John",
        last_name="Doe",
        phone="+1234567890",
        email="john@example.com"
    )
    
    assert guest.first_name == "John"
    assert guest.last_name == "Doe"
    assert guest.phone == "+1234567890"
    assert guest.email == "john@example.com"


def test_reservation_creation():
    """Test reservation model creation."""
    guest = Guest(first_name="Jane", last_name="Smith")
    
    reservation = Reservation(
        id="123",
        guest=guest,
        check_in=datetime(2024, 1, 1, 15, 0),
        check_out=datetime(2024, 1, 3, 11, 0),
        status="confirmed",
        property_id="prop_1"
    )
    
    assert reservation.id == "123"
    assert reservation.guest_name == "Jane Smith"
    assert reservation.status == "confirmed"


def test_visitor_creation():
    """Test visitor model creation."""
    visitor = Visitor(
        name="Test Guest",
        pin="1234"
    )
    
    assert visitor.name == "Test Guest"
    assert visitor.pin == "1234"


def test_visitor_validation():
    """Test visitor validation."""
    with pytest.raises(ValueError):
        Visitor(name="", pin="1234")  # Empty name
    
    with pytest.raises(ValueError):
        Visitor(name="Test", pin="12")  # Short PIN