"""The home page. This file includes examples abstracting complex UI into smaller components."""

import reflex as rx

from give_and_take.layouts import navbar, add_barter_layout


def home() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        navbar(),
        rx.grid(
            rx.card(
                "Give",
                size="3",
            ),
            rx.card(
                "Take",
                size="3",
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),
        rx.grid(
            columns="2",
            spacing="4",
            width="100%",
        ),
        add_barter_layout.event_form(),
        align="center",
        direction="column",
        spacing="2",
        width="100%",
    )
