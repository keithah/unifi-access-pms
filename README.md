# UniFi Access PMS

Universal Property Management Access Control Integration System

A flexible, plugin-based system that integrates UniFi Access with multiple property management systems to automate guest door access management through PIN codes.

## Features

- 🏗️ **Plugin-Based Architecture**: Extensible provider system for different PMS platforms
- 🏨 **Multi-Provider Support**: Hospitable, ICS calendar feeds, and extensible to other platforms
- 🔔 **Multi-Channel Notifications**: Simplepush, Matrix, Slack, Discord support
- 🔐 **Secure Configuration**: Encrypted credential storage with environment variable support
- ⚡ **Real-Time Updates**: Webhook support for instant synchronization
- 🎯 **Flexible PIN Generation**: Phone-based, random, or custom algorithms
- 📊 **Comprehensive CLI**: Full command-line interface for all operations

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/unifi-access-pms.git
cd unifi-access-pms

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### 2. Configuration

Generate a sample configuration:

```bash
unifi-access-pms create-config --output config.yaml
```

Edit the configuration with your credentials:

```yaml
core:
  enabled_providers: [hospitable, ics]
  pin_generation_method: phone_based
  
unifi:
  api_host: https://your-unifi-controller.local
  api_token: your_unifi_api_token
  
providers:
  hospitable:
    enabled: true
    config:
      api_key: your_hospitable_api_key
      property_mappings:
        property1: door_group1
        
  ics:
    enabled: true
    config:
      feeds:
        airbnb: https://airbnb.com/calendar.ics
        
notifications:
  enabled_channels: [simplepush]
  channels:
    simplepush:
      enabled: true
      config:
        key: your_simplepush_key
```

### 3. Testing

Test your configuration:

```bash
# Validate configuration
unifi-access-pms validate-config

# Test providers
unifi-access-pms test-providers

# Test notifications
unifi-access-pms test-notifications
```

### 4. Running

Synchronize reservations:

```bash
# Run sync with all enabled providers
unifi-access-pms sync

# Run specific providers only
unifi-access-pms sync --providers hospitable,ics

# Dry run to see what would happen
unifi-access-pms sync --dry-run
```

## Supported Providers

### Hospitable
- Full API integration with OAuth/API key support
- Real-time webhook updates
- Property mapping to door groups
- Guest information extraction

### ICS Calendar Feeds
- Universal ICS/iCal feed support
- Multiple feed aggregation
- Smart guest information parsing
- Timezone support

### Extensible Framework
- Plugin system for custom providers
- Standardized provider interface
- Dynamic provider loading

## Notification Channels

### Simplepush
Simple push notifications to mobile devices.

### Matrix
Decentralized messaging with rich formatting support.

### Slack
Workspace integration with rich attachments and fields.

### Discord
Server integration with embeds and custom formatting.

## CLI Commands

### Core Operations
```bash
# Standard execution
unifi-access-pms sync

# Verbose output
unifi-access-pms sync -v

# Specific providers
unifi-access-pms sync --providers hospitable,ics

# Date range
unifi-access-pms sync --date-range 2024-01-01:2024-01-31

# Dry run
unifi-access-pms sync --dry-run
```

### Configuration Management
```bash
# Create sample config
unifi-access-pms create-config

# Validate configuration
unifi-access-pms validate-config

# List providers
unifi-access-pms list-providers
```

### Testing
```bash
# Test all providers
unifi-access-pms test-providers

# Test notifications
unifi-access-pms test-notifications
```

## Configuration Reference

### Core Settings
- `enabled_providers`: List of active providers
- `pin_generation_method`: Algorithm for PIN codes
- `sync_interval`: Automatic sync frequency
- `timezone`: Default timezone

### Provider Configuration
Each provider has its own configuration section with:
- `enabled`: Enable/disable the provider
- `config`: Provider-specific settings
- `priority`: Processing priority
- `retry_attempts`: Failure retry count

### Notification Settings
- `enabled_channels`: Active notification channels
- `channels`: Channel-specific configurations
- `events`: Event types to send notifications for

### Security Features
- Credential encryption at rest
- Environment variable substitution
- Secure API token management
- Audit logging

## Development

### Project Structure
```
src/unifi_access_pms/
├── core/           # Core interfaces and models
├── config/         # Configuration management
├── providers/      # PMS provider implementations
├── notifications/  # Notification channels
└── cli.py         # Command-line interface
```

### Adding New Providers
1. Implement the `ReservationProvider` interface
2. Register in the provider registry
3. Add configuration schema
4. Test with the CLI

### Adding Notification Channels
1. Implement the `NotificationChannel` interface
2. Register in the notification registry
3. Add to the notification manager
4. Test with CLI commands

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the sample configurations