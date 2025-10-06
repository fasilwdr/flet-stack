"""
flet-stack: Decorator-based routing with view stacking for Flet applications.

A lightweight routing library that provides:
- Decorator-based route definitions
- Automatic view stacking from URL paths
- Built-in state management
- Async loading support
- URL parameter extraction
"""

__version__ = "0.1.0"
__author__ = "Fasil"
__email__ = "fasilwdr@hotmail.com"
__license__ = "MIT"

from .router import (
    view,
    enable_auto_routing,
    run_with_auto_routing,
    ViewPattern,
    VIEW_REGISTRY,
)

__all__ = [
    "view",
    "enable_auto_routing",
    "run_with_auto_routing",
    "ViewPattern",
    "VIEW_REGISTRY",
]