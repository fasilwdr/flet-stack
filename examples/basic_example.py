"""
Basic example demonstrating simple routing with flet-stack.
"""
import asyncio
import flet as ft
from flet_stack import view, FletStack


@view("/", appbar=ft.AppBar())
@ft.component
def home_view():
    return [ft.Column(
        [
            ft.Text("Home Page", size=40, weight=ft.FontWeight.BOLD),
            ft.Text("Welcome to flet-stack!", size=20),
            ft.Divider(),
            ft.Button(
                "Go to About",
                on_click=lambda _: asyncio.create_task(
                    ft.context.page.push_route("/about")
                ),
                icon=ft.Icons.INFO,
            ),
            ft.Button(
                "Go to Contact",
                on_click=lambda _: asyncio.create_task(
                    ft.context.page.push_route("/contact")
                ),
                icon=ft.Icons.CONTACT_MAIL,
            ),
            ft.Button(
                "View User Profile",
                on_click=lambda _: asyncio.create_task(
                    ft.context.page.push_route("/user/123")
                ),
                icon=ft.Icons.PERSON,
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )]


@view("/about", appbar=ft.AppBar())
@ft.component
def about_view():
    return [
        ft.Text("About Page", size=40, weight=ft.FontWeight.BOLD),
        ft.Text("This is a simple example of flet-stack routing.", size=16)
    ]


@view("/contact", appbar=ft.AppBar())
@ft.component
def contact_view():
    return [
        ft.Text("Contact Page", size=40, weight=ft.FontWeight.BOLD),
        ft.Text("Email: contact@example.com", size=16),
        ft.Text("Phone: +1 234 567 8900", size=16),
    ]


@view("/user/{user_id}", appbar=ft.AppBar())
@ft.component
def user_view(user_id):
    return [
        ft.Text("User Profile", size=40, weight=ft.FontWeight.BOLD),
        ft.Text(f"User ID: {user_id}", size=20),
    ]


def main(page: ft.Page):
    page.title = "flet-stack Basic Example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.render_views(FletStack)


if __name__ == "__main__":
    ft.run(main)
