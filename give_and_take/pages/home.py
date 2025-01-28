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
                self.style = {"background": "highlight"} if barter.give_done else {"background": "accent"}
            else:
                barter.take_done = not barter.take_done
                self.style = {"background": "highlight"} if barter.take_done else {"background": "accent"}
            session.add(barter)
            session.commit()

    @classmethod
    def get_component(cls, **props):
        barter = props.pop("barter")
        return rx.cond(
            barter.bargainer_id == AuthState.user.id,
            rx.card(
                barter.give,
                on_click=cls.toggle_done(barter, True),
                style=cls.style
            ),
            rx.cond(
                barter.bargainee_id == AuthState.user.id,
                rx.card(
                    barter.take,
                    on_click=cls.toggle_done(barter, False),
                    style=cls.style,
                ),
            ),
        )

class BarterRow(rx.ComponentState):
    style: dict[str, str] = {"background": "accent"}

    @rx.event
    def toggle_done(self, barter: Barter, is_give: bool):
        with rx.session() as session:
            barter = session.exec(Barter.select().where(Barter.id == barter.id)).first()
            if is_give:
                barter.give_done = not barter.give_done
                self.style = {"background": "highlight"} if barter.give_done else {"background": "accent"}
            else:
                barter.take_done = not barter.take_done
                self.style = {"background": "highlight"} if barter.take_done else {"background": "accent"}
            session.add(barter)
            session.commit()


    @classmethod
    def get_component(cls, **props):
        barter = props.pop("barter")
        return rx.cond(
            barter.bargainer_id == AuthState.user.id,
            rx.table.row(
                rx.table.cell(
                    barter.give,
                    on_click=cls.toggle_done(barter, True),
                    style=cls.style
                ),
                rx.table.cell(
                    barter.take,
                    style=cls.style,
                ),
            ),
            rx.cond(
                barter.bargainee_id == AuthState.user.id,
                rx.table.row(
                    rx.table.cell(
                        barter.take,
                        on_click=cls.toggle_done(barter, False),
                        style=cls.style,
                    ),
                    rx.table.cell(
                        barter.give,
                        style=cls.style,
                    ),
                ),
            ),
        )


barter_row = BarterRow.create
barter_cell = BarterCell.create

def home() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        navbar(),
        rx.vstack(
            rx.hstack(
                rx.card("Give"),
                rx.card("Take"),

            ),
            rx.hstack(
                rx.foreach(
                    HomeState.barters,
                    rx.button('hi'),
                ),

            ),
            width="80%",
        ),
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
                    lambda barter: barter_row(barter=barter),
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
