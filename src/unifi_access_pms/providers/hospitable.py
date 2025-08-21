"""Hospitable provider implementation."""

from typing import List, Dict, Any
from datetime import datetime

from ..core.interfaces import ReservationProvider
from ..core.models import Reservation, Guest


class HospitableProvider(ReservationProvider):
    """Hospitable reservation provider."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Hospitable provider."""
        self.config = config
        self.api_key = config.get('api_key')
        if not self.api_key:
            raise ValueError("Hospitable API key is required")
    
    def get_reservations(self, start_date: datetime, end_date: datetime) -> List[Reservation]:
        """Fetch reservations from Hospitable."""
        try:
            from hospitable_sdk import HospitableSDK
        except ImportError:
            raise ImportError("hospitable_sdk is required for Hospitable provider")
        
        sdk = HospitableSDK(api_key=self.api_key)
        
        # Get reservations
        reservations = []
        hospitable_reservations = sdk.reservations.list(
            start_date=start_date.date(),
            end_date=end_date.date()
        )
        
        for res in hospitable_reservations:
            if res.status == 'confirmed':
                guest = Guest(
                    first_name=res.guest.first_name or '',
                    last_name=res.guest.last_name or '',
                    phone=res.guest.phone,
                    email=res.guest.email
                )
                
                reservation = Reservation(
                    id=str(res.id),
                    guest=guest,
                    check_in=res.check_in,
                    check_out=res.check_out,
                    status=res.status,
                    property_id=str(res.property_id),
                    property_name=getattr(res, 'property_name', None)
                )
                reservations.append(reservation)
        
        return reservations
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate Hospitable provider configuration."""
        required_fields = ['api_key']
        return all(field in config for field in required_fields)