"""UniFi Access integration implementation."""

from typing import List, Dict, Any
from datetime import datetime

from ..core.interfaces import UniFiAccessIntegration
from ..core.models import Visitor


class UniFiAccessClient(UniFiAccessIntegration):
    """UniFi Access client implementation."""
    
    def __init__(self, host: str, token: str):
        """Initialize UniFi Access client."""
        self.host = host
        self.token = token
        self._client = None
    
    def _get_client(self):
        """Get or create UniFi Access client."""
        if self._client is None:
            try:
                from unifi_access import UniFiAccess
                self._client = UniFiAccess(host=self.host, token=self.token)
            except ImportError:
                raise ImportError("unifi_access_python is required for UniFi Access integration")
        return self._client
    
    def get_visitors(self) -> List[Visitor]:
        """Get all current visitors."""
        client = self._get_client()
        visitors = []
        
        unifi_visitors = client.visitors.list()
        for uv in unifi_visitors:
            visitor = Visitor(
                id=str(uv.id),
                name=uv.name,
                start_time=uv.start_time,
                end_time=uv.end_time,
                pin=getattr(uv, 'pin', ''),
                status=getattr(uv, 'status', 'active')
            )
            visitors.append(visitor)
        
        return visitors
    
    def create_visitor(self, visitor: Visitor) -> str:
        """Create a new visitor and return the visitor ID."""
        client = self._get_client()
        
        result = client.visitors.create(
            name=visitor.name,
            start_time=visitor.start_time,
            end_time=visitor.end_time,
            pin=visitor.pin
        )
        
        return str(result.id)
    
    def update_visitor(self, visitor_id: str, visitor: Visitor) -> bool:
        """Update an existing visitor."""
        client = self._get_client()
        
        try:
            client.visitors.update(
                visitor_id=visitor_id,
                name=visitor.name,
                start_time=visitor.start_time,
                end_time=visitor.end_time,
                pin=visitor.pin
            )
            return True
        except Exception:
            return False
    
    def delete_visitor(self, visitor_id: str) -> bool:
        """Delete a visitor."""
        client = self._get_client()
        
        try:
            client.visitors.delete(visitor_id)
            return True
        except Exception:
            return False