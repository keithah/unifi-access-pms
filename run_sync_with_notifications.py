#!/usr/bin/env python3
"""
UniFi Access PMS Synchronization with Notifications
Securely syncs Hospitable reservations with UniFi Access door control.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# Load configuration from environment variables
from config_loader import load_config

try:
    from hospitable_sdk import HospitableSDK
    from unifi_access import UniFiAccess
    import requests
except ImportError as e:
    print(f"❌ Missing required dependency: {e}")
    print("Install with: pip install hospitable-sdk unifi-access-python requests")
    sys.exit(1)


def generate_pin_from_phone(phone: str, length: int = 4) -> str:
    """Generate a PIN from phone number digits."""
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) >= length:
        return digits[-length:]
    else:
        # Pad with zeros if not enough digits
        return digits.zfill(length)


def send_notification(message: str, config: Dict[str, Any]) -> None:
    """Send push notification via Simplepush."""
    simplepush_key = os.getenv('SIMPLEPUSH_KEY')
    if not simplepush_key:
        print("ℹ️ No SIMPLEPUSH_KEY set, skipping notification")
        return
    
    try:
        response = requests.post(
            'https://api.simplepush.io/send',
            data={
                'key': simplepush_key,
                'title': 'UniFi Access Sync',
                'msg': message
            }
        )
        if response.status_code == 200:
            print(f"📱 Notification sent: {message}")
        else:
            print(f"⚠️ Notification failed: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Notification error: {e}")


def main():
    """Main synchronization function."""
    print("🔄 Starting UniFi Access PMS Sync")
    
    # Load configuration from environment variables
    try:
        config = load_config()
        hospitable_config = config['hospitable']
        unifi_config = config['unifi']
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please set the required environment variables or copy .env.example to .env")
        return
    
    # Initialize SDKs
    try:
        hospitable = HospitableSDK(api_key=hospitable_config['api_key'])
        unifi = UniFiAccess(
            host=unifi_config['api_host'],
            token=unifi_config['api_token']
        )
    except Exception as e:
        print(f"❌ SDK initialization failed: {e}")
        return
    
    # Get current reservations
    try:
        print("📋 Fetching Hospitable reservations...")
        reservations = hospitable.reservations.list(
            property_id=hospitable_config['property_id'],
            start_date=datetime.now().date(),
            end_date=(datetime.now() + timedelta(days=30)).date()
        )
        print(f"Found {len(reservations)} reservations")
    except Exception as e:
        print(f"❌ Failed to fetch reservations: {e}")
        return
    
    # Get current UniFi visitors
    try:
        print("👥 Fetching UniFi Access visitors...")
        visitors = unifi.visitors.list()
        print(f"Found {len(visitors)} current visitors")
    except Exception as e:
        print(f"❌ Failed to fetch visitors: {e}")
        return
    
    # Sync logic
    synced = 0
    created = 0
    updated = 0
    deleted = 0
    
    # Track processed reservations
    processed_guests = set()
    
    for reservation in reservations:
        if reservation.status == 'confirmed':
            guest_name = f"{reservation.guest.first_name} {reservation.guest.last_name}"
            guest_phone = reservation.guest.phone or ""
            
            # Generate PIN from phone
            pin = generate_pin_from_phone(guest_phone)
            
            # Check if visitor already exists
            existing_visitor = None
            for visitor in visitors:
                if visitor.name == guest_name:
                    existing_visitor = visitor
                    break
            
            if existing_visitor:
                # Update existing visitor
                try:
                    unifi.visitors.update(
                        visitor_id=existing_visitor.id,
                        start_time=reservation.check_in,
                        end_time=reservation.check_out,
                        pin=pin
                    )
                    updated += 1
                    print(f"✅ Updated visitor: {guest_name}")
                except Exception as e:
                    print(f"⚠️ Failed to update {guest_name}: {e}")
            else:
                # Create new visitor
                try:
                    unifi.visitors.create(
                        name=guest_name,
                        start_time=reservation.check_in,
                        end_time=reservation.check_out,
                        pin=pin
                    )
                    created += 1
                    print(f"✅ Created visitor: {guest_name}")
                except Exception as e:
                    print(f"⚠️ Failed to create {guest_name}: {e}")
            
            processed_guests.add(guest_name)
            synced += 1
    
    # Clean up cancelled/expired visitors
    for visitor in visitors:
        if visitor.name not in processed_guests:
            try:
                unifi.visitors.delete(visitor.id)
                deleted += 1
                print(f"🗑️ Deleted visitor: {visitor.name}")
            except Exception as e:
                print(f"⚠️ Failed to delete {visitor.name}: {e}")
    
    # Summary
    summary = f"Sync complete: {synced} processed, {created} created, {updated} updated, {deleted} deleted"
    print(f"✅ {summary}")
    
    # Send notification
    send_notification(summary, config)


if __name__ == "__main__":
    main()