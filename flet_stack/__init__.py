"""
flet-stack: A simple routing package for Flet applications.

This package provides decorator-based routing for Flet v1 applications with
support for stack navigation and view management.

Usage:
    from flet_stack import route, FletStack

    @route('/')
    def home_view():
        return ft.View(...)

    ft.run(lambda page: page.render_views(FletStack))
"""

from .router import route, FletStack

__version__ = "0.1.0"
__all__ = ["route", "FletStack"]