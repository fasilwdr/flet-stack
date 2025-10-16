"""
Advanced example demonstrating state management and async data loading with flet-stack.
"""

import asyncio
from dataclasses import dataclass
import flet as ft
from flet_stack import view, FletStack


# --- Counter Example with State Management ---
@ft.observable
@dataclass
class CounterState:
    count = 0

    def increment(self, e):
        self.count += 1

    def decrement(self, e):
        self.count -= 1


@view(route="/", state_class=CounterState, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
@ft.component
def home_view(state):
    return [
        ft.Text("Counter App", size=40, weight=ft.FontWeight.BOLD),
        ft.Text(f"Count: {state.count}", size=30),
        ft.Row(
            [
                ft.Button("Decrement", on_click=state.decrement, icon=ft.Icons.REMOVE),
                ft.Button("Increment", on_click=state.increment, icon=ft.Icons.ADD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Divider(),
        ft.Button(
            "View Products",
            on_click=lambda _: asyncio.create_task(
                ft.context.page.push_route("/products")
            ),
            icon=ft.Icons.SHOPPING_CART,
        ),
        ft.Button(
            "View User 42",
            on_click=lambda _: asyncio.create_task(
                ft.context.page.push_route("/user/42")
            ),
            icon=ft.Icons.PERSON,
        ),
    ]


# --- Products List with Async Loading ---
@ft.observable
@dataclass
class ProductsState:
    products = []


async def load_products(state):
    """Simulate loading products from an API"""
    await asyncio.sleep(2)  # Simulate network delay
    state.products = [
        {"id": 1, "name": "Laptop", "price": 999},
        {"id": 2, "name": "Mouse", "price": 29},
        {"id": 3, "name": "Keyboard", "price": 79},
        {"id": 4, "name": "Monitor", "price": 299},
    ]


@view("/products", state_class=ProductsState, on_load=load_products, appbar=ft.AppBar())
@ft.component
def products_view(state):
    def on_click_product(e):
        asyncio.create_task(
            ft.context.page.push_route(f"/products/{e.control.data}")
        )
    return [
        ft.Text("Products", size=40, weight=ft.FontWeight.BOLD),
        ft.Text("Available items:", size=16),
        ft.Divider(),
        ft.ListView(
            expand=True,
            controls=[
                ft.Card(
                    ft.Container(
                        ft.Column(
                            [
                                ft.Text(product["name"], size=20, weight=ft.FontWeight.BOLD),
                                ft.Text(f"${product['price']}", size=16),
                                ft.Button(
                                    "View Details",
                                    data=product['id'],
                                    on_click=on_click_product
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
    ]


# --- Product Detail with URL Parameter ---
@ft.observable
@dataclass
class ProductDetailState:
    product = None


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
    "/products/{product_id}", state_class=ProductDetailState, on_load=load_product_detail, appbar=ft.AppBar()
)
@ft.component
def product_detail_view(state, product_id):
    return [
        ft.Text("Product Details", size=40, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text(state.product["name"], size=30),
        ft.Text(f"Price: ${state.product['price']}", size=20),
        ft.Text(
            state.product.get("description", "No description"),
            size=16,
            color=ft.Colors.GREY,
        )
    ]


# --- User Profile with Async Loading ---
class UserState:
    user = None


async def load_user(state, user_id):
    """Simulate loading user data from an API"""
    await asyncio.sleep(1.5)
    state.user = {
        "id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com",
        "joined": "2024-01-15",
    }


@view("/user/{user_id}", state_class=UserState, on_load=load_user, appbar=ft.AppBar())
@ft.component
def user_view(state, user_id):
    return [
        ft.Text("User Profile", size=40, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text(f"Name: {state.user['name']}", size=20),
        ft.Text(f"Email: {state.user['email']}", size=16),
        ft.Text(f"User ID: {state.user['id']}", size=16),
        ft.Text(f"Joined: {state.user['joined']}", size=16, color=ft.Colors.GREY),
    ]


def main(page: ft.Page):
    page.title = "flet-stack Advanced Example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.render_views(FletStack)


if __name__ == "__main__":
    ft.run(main)
