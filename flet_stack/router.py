import asyncio
import re
import inspect

import flet as ft


# --- Decorator & Router Implementation ---

class ViewPattern:
    def __init__(self, pattern, state_class, func, on_load, view_kwargs):
        self.pattern = pattern
        self.state_class = state_class
        self.func = func
        self.on_load = on_load
        self.view_kwargs = view_kwargs
        regex_pat = re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", pattern)
        self.regex = re.compile(f"^{regex_pat}$")

    def match(self, route):
        return self.regex.match(route)

    def build(self, page, **kwargs):
        state = self.state_class() if self.state_class else None

        loading_control = ft.Container(
            alignment=ft.Alignment.CENTER,
            content=ft.ProgressRing(stroke_width=5, color=ft.Colors.PRIMARY_CONTAINER)
        )

        v = ft.View(
            route=page.route,
            controls=[loading_control],
            **self.view_kwargs
        )
        # Prepare argument map for view function
        arg_map = {
            "state": state,
            "page": page,
            **kwargs,
        }

        def show_actual_view():
            view_sig = inspect.signature(self.func)
            # Build argument list for the view function, only those which exist
            call_args = []
            for name, param in view_sig.parameters.items():
                call_args.append(arg_map.get(name, param.default if param.default != inspect.Parameter.empty else None))
            controls = [
                ft.StateView(
                    state,
                    lambda state: self.func(*call_args)
                )
            ]
            v.controls.clear()
            v.controls.extend(controls)
            page.update()

        def sync_loader():
            if self.on_load:
                sig = inspect.signature(self.on_load)
                arg_map = {
                    "state": state,
                    "page": page,
                    "view": v,
                    **kwargs,
                }
                actual_args = [arg_map.get(name, None) for name in sig.parameters]
                self.on_load(*actual_args)
            # After on_load, update the UI in event loop via a coroutine
            async def async_show_actual_view():
                show_actual_view()
            page.run_task(async_show_actual_view)

        async def async_loader():
            if self.on_load:
                sig = inspect.signature(self.on_load)
                arg_map = {
                    "state": state,
                    "page": page,
                    "view": v,
                    **kwargs,
                }
                actual_args = [arg_map.get(name, None) for name in sig.parameters]
                await self.on_load(*actual_args)
            show_actual_view()

        if self.on_load:
            if asyncio.iscoroutinefunction(self.on_load):
                page.run_task(async_loader)
            else:
                page.run_thread(sync_loader)
        else:
            show_actual_view()

        return v


VIEW_REGISTRY = []


def view(route, state_class=None, on_load=None, **view_kwargs):
    def decorator(func):
        vp = ViewPattern(route, state_class, func, on_load, view_kwargs)
        VIEW_REGISTRY.append(vp)
        return func

    return decorator


_original_run = ft.run


def enable_auto_routing(page: ft.Page):
    # Track the last processed route to prevent duplicate processing
    last_processed_route = {"route": None}

    def on_route_change(e):
        # Prevent duplicate processing of the same route
        current_route = page.route
        if last_processed_route["route"] == current_route:
            return

        last_processed_route["route"] = current_route

        page.views.clear()
        segments = [seg for seg in page.route.strip("/").split("/") if seg]
        stack_routes = []
        for i in range(len(segments)):
            stack_routes.append("/" + "/".join(segments[: i + 1]))
        if not stack_routes:
            stack_routes = ["/"]

        for route in stack_routes:
            found = False
            for vp in VIEW_REGISTRY:
                m = vp.match(route)
                if m:
                    found = True
                    kwargs = m.groupdict()
                    prev_route = page.route
                    page.route = route
                    page.views.append(vp.build(page, **kwargs))
                    page.route = prev_route
                    break
            if not found:
                page.views.append(ft.View(route=route, controls=[ft.Text("404 Not Found")]))
        page.update()

    page.on_route_change = on_route_change


def run_with_auto_routing(main_func, *args, **kwargs):
    def wrapped_main(page: ft.Page, *a, **kw):
        enable_auto_routing(page)
        return main_func(page, *a, **kw)

    return _original_run(wrapped_main, *args, **kwargs)


ft.run = run_with_auto_routing