"""Shared auth layout."""

import reflex as rx


def container(*children, **props) -> rx.Component:
    """A fixed container based on a 960px grid."""
    # Enable override of default props.
    props = (
        dict(
            width="100%",
            max_width="960px",
            background="white",
            height="100%",
            px="9",
            margin="0 auto",
            position="relative",
        )
        | props
    )
    return rx.stack(*children, **props)


def auth_layout(*args) -> rx.Component:
    """The shared layout for the login and sign up pages."""
    return rx.box(
        container(
            rx.vstack(
                rx.heading("Welcome to Give and Take!", size="8"),
                align="center",
            ),
            *args,
            border_top_radius="10px",
            box_shadow="0 4px 60px 0 rgba(0, 0, 0, 0.08), 0 4px 16px 0 rgba(0, 0, 0, 0.08)",
            display="flex",
            flex_direction="column",
            align_items="center",
            padding_top="36px",
            padding_bottom="24px",
            spacing="4",
        ),
        height="100vh",
        padding_top="40px",
        background="url(bg.svg)",
        background_repeat="no-repeat",
        background_size="cover",
    )
