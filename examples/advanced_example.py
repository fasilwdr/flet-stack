"""
Advanced example demonstrating state management and async data loading with flet-stack.
"""

import asyncio
import flet as ft
from flet_stack import view


# --- Counter Example with State Management ---
class CounterState:
    def __init__(self):
        self.count = 0


@view("/", state_class=CounterState)
def home_view(state, page):
    def increment(e):
        state.count += 1
        page.update()

    def decrement(e):
        state.count -= 1
        page.update()

    return ft.Column(
        [
            ft.Text("Counter App", size=40, weight=ft.FontWeight.BOLD),
            ft.Text(f"Count: {state.count}", size=30),
            ft.Row(
                [
                    ft.Button("Decrement", on_click=decrement, icon=ft.Icons.REMOVE),
                    ft.Button("Increment", on_click=increment, icon=ft.Icons.ADD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(),
            ft.Button(
                "View Products",
                on_click=lambda _: page.go("/products"),
                icon=ft.Icons.SHOPPING_CART,
            ),
            ft.Button(
                "View User 42",
                on_click=lambda _: page.go("/user/42"),
                icon=ft.Icons.PERSON,
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


# --- Products List with Async Loading ---
class ProductsState:
    def __init__(self):
        self.products = []


async def load_products(state):
    """Simulate loading products from an API"""
    await asyncio.sleep(2)  # Simulate network delay
    state.products = [
        {"id": 1, "name": "Laptop", "price": 999},
        {"id": 2, "name": "Mouse", "price": 29},
        {"id": 3, "name": "Keyboard", "price": 79},
        {"id": 4, "name": "Monitor", "price": 299},
    ]


@view("/products", state_class=ProductsState, on_load=load_products)
def products_view(state, page):
    return ft.Column(
        [
            ft.Text("Products", size=40, weight=ft.FontWeight.BOLD),
            ft.Text("Available items:", size=16),
            ft.Divider(),
            ft.Column(
                [
                    ft.Card(
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Text(product["name"], size=20, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"${product['price']}", size=16),
                                    ft.Button(
                                        "View Details",
                                        on_click=lambda _, pid=product["id"]: page.go(
                                            f"/products/{pid}"
                                        ),
                                    ),
                                ]
                            ),
                            padding=15,
                        )
                    )
                    for product in state.products
                ],
                spacing=10,
            ),
            ft.Divider(),
            ft.Button(
                "Back to Home", on_click=lambda _: page.go("/"), icon=ft.Icons.HOME
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )


# --- Product Detail with URL Parameter ---
class ProductDetailState:
    def __init__(self):
        self.product = None


async def load_product_detail(state, product_id):
    """Simulate loading product detail from an API"""
    await asyncio.sleep(1)
    # Simulate fetching product by ID
    products = {
        "1": {"id": 1, "name": "Laptop", "price": 999, "description": "High-performance laptop"},
        "2": {"id": 2, "name": "Mouse", "price": 29, "description": "Wireless ergonomic mouse"},
        "3": {"id": 3, "name": "Keyboard", "price": 79, "description": "Mechanical keyboard"},
        "4": {"id": 4, "name": "Monitor", "price": 299, "description": "27-inch 4K monitor"},
    }
    state.product = products.get(product_id, {"name": "Not Found", "price": 0})


@view(
    "/products/{product_id}", state_class=ProductDetailState, on_load=load_product_detail
)
def product_detail_view(state, page, product_id):
    return ft.Column(
        [
            ft.Text("Product Details", size=40, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(state.product["name"], size=30),
            ft.Text(f"Price: ${state.product['price']}", size=20),
            ft.Text(
                state.product.get("description", "No description"),
                size=16,
                color=ft.Colors.GREY,
            ),
            ft.Divider(),
            ft.Row(
                [
                    ft.Button(
                        "Back to Products",
                        on_click=lambda _: page.go("/products"),
                        icon=ft.Icons.ARROW_BACK,
                    ),
                    ft.Button(
                        "Home", on_click=lambda _: page.go("/"), icon=ft.Icons.HOME
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


# --- User Profile with Async Loading ---
class UserState:
    def __init__(self):
        self.user = None


async def load_user(state, user_id):
    """Simulate loading user data from an API"""
    await asyncio.sleep(1.5)
    state.user = {
        "id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com",
        "joined": "2024-01-15",
    }


@view("/user/{user_id}", state_class=UserState, on_load=load_user)
def user_view(state, page, user_id):
    return ft.Column(
        [
            ft.Text("User Profile", size=40, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"Name: {state.user['name']}", size=20),
            ft.Text(f"Email: {state.user['email']}", size=16),
            ft.Text(f"User ID: {state.user['id']}", size=16),
            ft.Text(f"Joined: {state.user['joined']}", size=16, color=ft.Colors.GREY),
            ft.Divider(),
            ft.Button(
                "Back to Home", on_click=lambda _: page.go("/"), icon=ft.Icons.HOME
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def main(page: ft.Page):
    page.title = "flet-stack Advanced Example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.go("/")


if __name__ == "__main__":
    ft.run(main)