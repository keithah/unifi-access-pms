#!/usr/bin/env python3
"""
Secure configuration loader for UniFi Access PMS.
Loads configuration from environment variables to avoid hardcoded credentials.
"""

import os
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    
    required_vars = [
        'HOSPITABLE_API_KEY',
        'HOSPITABLE_PROPERTY_NAME', 
        'HOSPITABLE_PROPERTY_ID',
        'UNIFI_API_HOST',
        'UNIFI_API_TOKEN'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return {
        'hospitable': {
            'api_key': os.getenv('HOSPITABLE_API_KEY'),
            'property_name': os.getenv('HOSPITABLE_PROPERTY_NAME'),
            'property_id': os.getenv('HOSPITABLE_PROPERTY_ID')
        },
        'unifi': {
            'api_host': os.getenv('UNIFI_API_HOST'),
            'api_token': os.getenv('UNIFI_API_TOKEN')
        }
    }


if __name__ == "__main__":
    try:
        config = load_config()
        print("✅ Configuration loaded successfully")
        print(f"Hospitable property: {config['hospitable']['property_name']}")
        print(f"UniFi host: {config['unifi']['api_host']}")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please set the required environment variables or copy .env.example to .env")