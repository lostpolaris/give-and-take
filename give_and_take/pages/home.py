"""The home page. This file includes examples abstracting complex UI into smaller components."""

import reflex as rx

from give_and_take.layouts import navbar, add_barter_layout
from give_and_take.state import HomeState, AuthState


def create_barter_row(barter) -> rx.Component:
    return rx.cond(
        barter.bargainer_id == AuthState.user.id,
        rx.table.row(
            rx.table.cell(barter.give),
            rx.table.cell(barter.take),
        ),
        rx.table.row(
            rx.table.cell(barter.take),
            rx.table.cell(barter.give),
        ),
    )


def home() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        navbar(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.cell("Gives"),
                    rx.table.cell("Takes"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    HomeState.barters,
                    lambda barter: create_barter_row(barter),
                ),
            ),
            width="100%",
        ),
        add_barter_layout.event_form(),
        rx.button("Refresh Barters", on_click=HomeState.get_barters),
        align="center",
        direction="column",
        spacing="2",
        width="100%",
        on_mount=HomeState.get_barters,
    )
