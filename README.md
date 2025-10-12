# flet-stack

**Decorator-based routing with automatic view stacking for Flet applications.**

[![PyPI version](https://badge.fury.io/py/flet-stack.svg)](https://badge.fury.io/py/flet-stack)
[![Python versions](https://img.shields.io/pypi/pyversions/flet-stack.svg)](https://pypi.org/project/flet-stack/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/flet-stack?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/flet-stack)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🎯 **Decorator-based routing** - Clean, intuitive `@view()` decorator for route definitions
- 📚 **Automatic view stacking** - Navigate `/users/123/profile` and get a stack of 3 views
- 🔄 **State management** - Built-in state classes with `StateView` integration
- ⚡ **Async support** - Handle async data loading with automatic loading indicators
- 🎨 **URL parameters** - Extract parameters from routes like `/user/{id}`
- 🚀 **Zero configuration** - Just replace `ft.run()` with auto-routing enabled

## Installation

### From PyPI

```bash
pip install flet-stack
```

### From GitHub

```bash
pip install git+https://github.com/fasilwdr/flet-stack.git
```

### Install Specific Version

```bash
pip install git+https://github.com/fasilwdr/flet-stack.git@v0.1.0
```

### From Source

```bash
git clone https://github.com/fasilwdr/flet-stack.git
cd flet-stack
pip install .
```

## Quick Start

```python
import flet as ft
from flet_stack import view

# Define your routes with the @view decorator
@view("/")
def home_view(page):
    return ft.Column([
        ft.Text("Home Page", size=30),
        ft.Button("Go to Profile", on_click=lambda _: page.go("/profile")),
    ])

@view("/profile")
def profile_view(page):
    return ft.Column([
        ft.Text("Profile Page", size=30),
        ft.Button("Back", on_click=lambda _: page.go("/")),
    ])

# Run your app with auto-routing
def main(page: ft.Page):
    page.title = "My Flet App"
    page.go("/")  # Navigate to home

ft.run(main)
```

That's it! The routing is automatically enabled.

## Advanced Usage

### URL Parameters

Extract parameters from your routes:

```python
@view("/user/{user_id}")
def user_view(page, user_id):
    return ft.Column([
        ft.Text(f"User Profile: {user_id}", size=30),
        ft.Button("Back", on_click=lambda _: page.go("/")),
    ])
```

### State Management

Use state classes to manage component state:

```python
class CounterState:
    def __init__(self):
        self.count = 0

@view("/counter", state_class=CounterState)
def counter_view(state, page):
    def increment(e):
        state.count += 1
        page.update()
    
    return ft.Column([
        ft.Text(f"Count: {state.count}", size=30),
        ft.Button("Increment", on_click=increment),
    ])
```

### Async Data Loading

Load data asynchronously before showing your view:

```python
class UserState:
    def __init__(self):
        self.user_data = None

async def load_user_data(state, user_id):
    # Simulate API call
    await asyncio.sleep(1)
    state.user_data = {"id": user_id, "name": f"User {user_id}"}

@view("/user/{user_id}", state_class=UserState, on_load=load_user_data)
def user_detail_view(state, page, user_id):
    return ft.Column([
        ft.Text(f"Name: {state.user_data['name']}", size=20),
        ft.Text(f"ID: {state.user_data['id']}", size=16),
    ])
```

While loading, a progress indicator is automatically displayed.

### View Configuration

Pass additional Flet view properties:

```python
@view(
    "/settings",
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    vertical_alignment=ft.MainAxisAlignment.CENTER,
    padding=20,
)
def settings_view(page):
    return ft.Text("Settings", size=30)
```

### View Stacking

Routes automatically create a navigation stack. Navigating to `/users/123/profile` creates:
- View 1: `/users`
- View 2: `/users/123`
- View 3: `/users/123/profile`

This enables natural back navigation in your app.

## How It Works

**flet-stack** patches `ft.run()` to automatically enable routing when your app starts. It:

1. Registers all `@view` decorated functions
2. Intercepts route changes
3. Builds a view stack from the URL path
4. Handles state management and async loading
5. Renders your views with proper navigation support

## Examples

Check the `examples/` directory for more detailed examples:
- `basic_example.py` - Simple routing and navigation
- `advanced_example.py` - State management, async loading, and URL parameters

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built on top of the amazing [Flet](https://docs.flet.dev) framework.

## Support

If you encounter any issues or have questions:
- Open an issue on [GitHub](https://github.com/fasilwdr/flet-stack/issues)
- Check the [examples](examples/) directory
- Read the [Flet documentation](https://docs.flet.dev/)