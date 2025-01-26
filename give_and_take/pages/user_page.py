"""The home page. This file includes examples abstracting complex UI into smaller components."""

import reflex as rx

from give_and_take.layouts import navbar


def user_page() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        navbar(),
        rx.card(
            "Give and Take3",
            justify="center",
            size="3",
            width="100%",
        ),
        rx.grid(
            rx.card("Give"),
            rx.card("Take"),
            columns="2",
            spacing="4",
            width="100%",
        ),
        rx.grid(
            columns="2",
            spacing="4",
            width="100%",
        ),
        rx.button("New Barter", color_scheme="grass", on_click=None),
        align="center",
        direction="column",
        spacing="2",
        width="100%",
    )
