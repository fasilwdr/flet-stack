"""
Basic example demonstrating simple routing with flet-stack.
"""

import flet as ft
from flet_stack import view


@view("/")
def home_view(page):
    return ft.Column(
        [
            ft.Text("Home Page", size=40, weight=ft.FontWeight.BOLD),
            ft.Text("Welcome to flet-stack!", size=20),
            ft.Divider(),
            ft.Button(
                "Go to About",
                on_click=lambda _: page.go("/about"),
                icon=ft.Icons.INFO,
            ),
            ft.Button(
                "Go to Contact",
                on_click=lambda _: page.go("/contact"),
                icon=ft.Icons.CONTACT_MAIL,
            ),
            ft.Button(
                "View User Profile",
                on_click=lambda _: page.go("/user/123"),
                icon=ft.Icons.PERSON,
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


@view("/about")
def about_view(page):
    return ft.Column(
        [
            ft.Text("About Page", size=40, weight=ft.FontWeight.BOLD),
            ft.Text("This is a simple example of flet-stack routing.", size=16),
            ft.Divider(),
            ft.Button(
                "Back to Home",
                on_click=lambda _: page.go("/"),
                icon=ft.Icons.HOME,
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


@view("/contact")
def contact_view(page):
    return ft.Column(
        [
            ft.Text("Contact Page", size=40, weight=ft.FontWeight.BOLD),
            ft.Text("Email: contact@example.com", size=16),
            ft.Text("Phone: +1 234 567 8900", size=16),
            ft.Divider(),
            ft.Button(
                "Back to Home",
                on_click=lambda _: page.go("/"),
                icon=ft.Icons.HOME,
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


@view("/user/{user_id}")
def user_view(page, user_id):
    return ft.Column(
        [
            ft.Text("User Profile", size=40, weight=ft.FontWeight.BOLD),
            ft.Text(f"User ID: {user_id}", size=20),
            ft.Divider(),
            ft.Button(
                "Back to Home",
                on_click=lambda _: page.go("/"),
                icon=ft.Icons.HOME,
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def main(page: ft.Page):
    page.title = "flet-stack Basic Example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.go("/")


if __name__ == "__main__":
    ft.run(main)