"""The home page. This file includes examples abstracting complex UI into smaller components."""

from typing import Optional

import reflex as rx

from give_and_take.layouts import navbar, add_barter_layout
from give_and_take.models import Barter
from give_and_take.state import HomeState, AuthState


class BarterRow(rx.ComponentState):
    color = {False: "white", True: "green"}

    @rx.event
    def toggle_done(self, barter: Barter, is_give: bool):
        with rx.session() as session:
            if is_give:
                barter = session.exec(
                    Barter.select().where(Barter.id == barter.id)
                ).first()
                barter.give_done = not barter.give_done
            else:
                barter = session.exec(
                    Barter.select().where(Barter.id == barter.id)
                ).first()
                barter.take_done = not barter.take_done
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
                    on_click=lambda: cls.toggle_done(barter, True),
                    style={"bg": cls.color[barter.give_done]},
                ),
                rx.table.cell(
                    barter.take,
                    style={"bg": cls.color[barter.take_done]},
                ),
            ),
            rx.table.row(
                rx.table.cell(
                    barter.take,
                    on_click=lambda: cls.toggle_done(barter, False),
                    style={"bg": cls.color[barter.take_done]},
                ),
                rx.table.cell(
                    barter.give,
                    style={"bg": cls.color[barter.give_done]},
                ),
            ),
        )


def home() -> rx.Component:
    # Welcome Page (Index)
    barter_row = BarterRow.create
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
                    lambda barter: barter_row(barter=barter),
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
