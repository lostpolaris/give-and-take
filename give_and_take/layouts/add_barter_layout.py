import reflex as rx

from give_and_take.state import BarterState


def form_field(label: str, placeholder: str, type: str, name: str) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.form.label(label),
            rx.form.control(
                rx.input(placeholder=placeholder, type=type),
                as_child=True,
            ),
            direction="column",
            spacing="1",
        ),
        name=name,
        width="100%",
    )


def event_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Create Barter")),
        rx.dialog.content(
            rx.dialog.title("Create Barter"),
            rx.dialog.description(
                "Create an exchange request.",
                size="2",
                margin_bottom="16px",
            ),
            rx.flex(
                rx.text(
                    "I Give",
                    as_="div",
                    size="2",
                    margin_bottom="4px",
                    weight="bold",
                ),
                rx.input(
                    default_value="",
                    on_blur=BarterState.set_give,
                    placeholder="What will you give?",
                ),
                rx.text(
                    "I Take",
                    as_="div",
                    size="2",
                    margin_bottom="4px",
                    weight="bold",
                ),
                rx.input(
                    default_value="",
                    on_blur=BarterState.set_take,
                    placeholder="What will you take?",
                ),
                rx.text(
                    "Who will you exchange with?",
                    as_="div",
                    size="2",
                    margin_bottom="4px",
                    weight="bold",
                ),
                rx.input(
                    default_value="",
                    on_blur=BarterState.set_bargainee,
                    placeholder="What will receive this barter?",
                ),
                direction="column",
                spacing="3",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        color_scheme="gray",
                        variant="soft",
                    ),
                ),
                # TODO: fix this
                rx.cond(
                    BarterState.success,
                    rx.dialog.close(
                        rx.button("Create Barter", on_click=BarterState.create_barter),
                    ),
                    rx.button("Attempt Barter", on_click=BarterState.attempt_barter),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
        ),
    )
