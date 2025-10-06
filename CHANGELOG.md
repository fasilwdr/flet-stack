# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-06

### Added
- Initial release of flet-stack
- `@view()` decorator for route definition
- Automatic view stacking from URL paths
- State management with `state_class` parameter
- Async loading support with `on_load` parameter
- URL parameter extraction (e.g., `/user/{id}`)
- Automatic loading indicators during async operations
- Support for custom view properties via `**view_kwargs`
- Automatic routing via patched `ft.run()`
- 404 handling for undefined routes
- Prevention of duplicate route processing

### Features
- Decorator-based routing
- Automatic view stack creation from nested paths
- Built-in state management
- Support for both sync and async `on_load` functions
- Flexible parameter injection for view functions
- Regex-based route matching with named groups

[0.1.0]: https://github.com/fasilwdr/flet-stack/releases/tag/v0.1.0