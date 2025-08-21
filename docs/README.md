# UniFi Access PMS Documentation

This directory contains comprehensive documentation for the UniFi Access PMS system.

## Contents

- **API Reference**: Complete API documentation for all modules
- **Configuration Guide**: Detailed configuration options and examples
- **Provider Integration**: How to integrate with different PMS providers
- **Notification Channels**: Setting up various notification channels
- **Deployment Guide**: Production deployment instructions
- **Troubleshooting**: Common issues and solutions

## Quick Links

- [Getting Started](getting-started.md)
- [Configuration Reference](configuration.md)
- [Provider Guide](providers.md)
- [API Documentation](api.md)

## Architecture

The UniFi Access PMS follows a plugin-based architecture:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PMS Provider  │───▶│  Core Engine     │───▶│ UniFi Access    │
│   (Hospitable)  │    │  (Sync Logic)    │    │  Integration    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Notifications   │
                       │  (Simplepush)    │
                       └──────────────────┘
```

## Contributing

See the main README.md for contribution guidelines.