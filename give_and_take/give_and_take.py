"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import asyncio

import reflex as rx
from reflex.components.radix.themes import theme

from .pages import home, login, signup, user_page
from .state import HomeState
from .state.base import State


async def a_get_barters():
    HomeState.get_barters()
    await asyncio.sleep(5)


app = rx.App(
    theme=theme(
        appearance="inherit", has_background=True, radius="large", accent_color="teal"
    )
)

app.add_page(login)
app.add_page(signup)
app.add_page(user_page, route="/user_page", on_load=State.check_login())
app.add_page(home, route="/", on_load=State.check_login())

app.register_lifespan_task(a_get_barters)
