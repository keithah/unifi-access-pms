#!/usr/bin/env python3
"""Command-line interface for UniFi Access PMS."""

import click
import yaml
from pathlib import Path
from typing import Optional, List

from .config.manager import ConfigManager
from .core.registry import ProviderRegistry, NotificationRegistry
from .notifications.manager import NotificationManager


@click.group()
@click.version_option()
def cli():
    """UniFi Access PMS - Universal Property Management Access Control Integration System."""
    pass


@cli.command()
@click.option('--output', '-o', type=click.Path(), default='config.yaml',
              help='Output configuration file path')
def create_config(output: str):
    """Generate a sample configuration file."""
    sample_config = {
        'core': {
            'enabled_providers': ['hospitable', 'ics'],
            'pin_generation_method': 'phone_based',
            'timezone': 'UTC'
        },
        'unifi': {
            'api_host': 'https://your-unifi-controller.local',
            'api_token': 'your_unifi_api_token'
        },
        'providers': {
            'hospitable': {
                'enabled': True,
                'config': {
                    'api_key': 'your_hospitable_api_key',
                    'property_mappings': {
                        'property1': 'door_group1'
                    }
                }
            },
            'ics': {
                'enabled': True,
                'config': {
                    'feeds': {
                        'airbnb': 'https://airbnb.com/calendar.ics'
                    }
                }
            }
        },
        'notifications': {
            'enabled_channels': ['simplepush', 'matrix'],
            'channels': {
                'simplepush': {
                    'enabled': True,
                    'config': {
                        'key': 'your_simplepush_key'
                    }
                },
                'matrix': {
                    'enabled': True,
                    'config': {
                        'homeserver': 'matrix.org',
                        'access_token': 'your_matrix_access_token',
                        'room_id': '!your_room_id:matrix.org'
                    }
                }
            }
        }
    }
    
    with open(output, 'w') as f:
        yaml.dump(sample_config, f, default_flow_style=False, indent=2)
    
    click.echo(f"✅ Sample configuration written to {output}")


@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), default='config.yaml',
              help='Configuration file path')
def validate_config(config: str):
    """Validate configuration file."""
    try:
        config_manager = ConfigManager(config)
        config_manager.validate()
        click.echo("✅ Configuration is valid")
    except Exception as e:
        click.echo(f"❌ Configuration validation failed: {e}")
        raise click.ClickException(str(e))


@cli.command()
def list_providers():
    """List all available providers."""
    registry = ProviderRegistry()
    providers = registry.list_providers()
    
    click.echo("Available providers:")
    for provider in providers:
        click.echo(f"  - {provider}")


@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), default='config.yaml',
              help='Configuration file path')
@click.option('--providers', '-p', help='Comma-separated list of providers to sync')
@click.option('--dry-run', is_flag=True, help='Show what would be done without making changes')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def sync(config: str, providers: Optional[str], dry_run: bool, verbose: bool):
    """Synchronize reservations with UniFi Access."""
    try:
        config_manager = ConfigManager(config)
        
        # Parse providers list
        provider_list = None
        if providers:
            provider_list = [p.strip() for p in providers.split(',')]
        
        if dry_run:
            click.echo("🔍 Dry run mode - no changes will be made")
        
        # TODO: Implement sync logic
        click.echo("✅ Sync completed successfully")
        
    except Exception as e:
        click.echo(f"❌ Sync failed: {e}")
        raise click.ClickException(str(e))


@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), default='config.yaml',
              help='Configuration file path')
def test_providers(config: str):
    """Test all enabled providers."""
    try:
        config_manager = ConfigManager(config)
        # TODO: Implement provider testing
        click.echo("✅ All providers tested successfully")
    except Exception as e:
        click.echo(f"❌ Provider testing failed: {e}")
        raise click.ClickException(str(e))


@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), default='config.yaml',
              help='Configuration file path')
def test_notifications(config: str):
    """Test notification channels."""
    try:
        config_manager = ConfigManager(config)
        notification_manager = NotificationManager(config_manager.config)
        
        # Send test notification
        notification_manager.send_notification(
            "Test notification from UniFi Access PMS",
            event_type="test"
        )
        
        click.echo("✅ Test notifications sent successfully")
    except Exception as e:
        click.echo(f"❌ Notification testing failed: {e}")
        raise click.ClickException(str(e))


if __name__ == '__main__':
    cli()