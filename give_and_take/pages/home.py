"""The home page. This file includes examples abstracting complex UI into smaller components."""

from typing import Optional
import logging

import reflex as rx

from give_and_take.layouts import navbar, add_barter_layout
from give_and_take.models import Barter
from give_and_take.state import HomeState, AuthState


class BarterCell(rx.ComponentState):
    style: dict[str, str] = {"background": "accent"}

    @rx.event
    def toggle_done(self, barter: Barter, is_give: bool):
        with rx.session() as session:
            barter = session.exec(Barter.select().where(Barter.id == barter.id)).first()
            if is_give:
                barter.give_done = not barter.give_done
                self.style = (
                    {"background": "highlight"}
                    if barter.give_done
                    else {"background": "accent"}
                )
            else:
                barter.take_done = not barter.take_done
                self.style = (
                    {"background": "highlight"}
                    if barter.take_done
                    else {"background": "accent"}
                )
            session.add(barter)
            session.commit()

    @classmethod
    def get_component(cls, **props):
        barter = props.pop("barter")
        is_give = props.pop("is_give")
        return rx.cond(
            is_give,
            rx.card(
                barter.give,
                on_click=cls.toggle_done(barter, is_give),
                width="100%",
                style=cls.style,
            ),
            rx.card(
                barter.take,
                on_click=cls.toggle_done(barter, is_give),
                width="100%",
                style=cls.style,
            ),
        )


barter_cell = BarterCell.create


def home() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        navbar(),
        rx.vstack(
            rx.hstack(
                rx.card("Gives", width="100%"),
                rx.card("Takes", width="100%"),
                width="100%",
            ),
            rx.foreach(
                HomeState.barters,
                lambda barter: rx.cond(
                    barter.bargainer_id == AuthState.user.id,
                    rx.hstack(
                        barter_cell(barter=barter, is_give=True),
                        barter_cell(barter=barter, is_give=False),
                        width="100%",
                    ),
                    rx.cond(
                        barter.bargainee_id == AuthState.user.id,
                        rx.hstack(
                            barter_cell(barter=barter, is_give=False),
                            barter_cell(barter=barter, is_give=True),
                            width="100%",
                        ),
                    ),
                ),
            ),
            width="80%",
        ),
        add_barter_layout.event_form(),
        rx.button("Refresh Barters", on_click=HomeState.get_barters),
        align="center",
        direction="column",
        spacing="2",
        width="100%",
        on_mount=HomeState.get_barters,
    )
