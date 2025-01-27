"""The home page. This file includes examples abstracting complex UI into smaller components."""

import reflex as rx

from give_and_take.layouts import navbar, add_barter_layout
from give_and_take.models import Barter
from give_and_take.state import HomeState, AuthState


class BarterRow(rx.ComponentState):
    @rx.event
    def mark_done(self, is_give: bool):
        with rx.session() as session:
            if is_give:
                session.exec(
                    Barter.update()
                    .where(Barter.id == self.barter.id)
                    .values(give_done=True)
                )
            else:
                session.exec(
                    Barter.update()
                    .where(Barter.id == self.barter.id)
                    .values(take_done=True)
                )
            session.commit()

    @classmethod
    def get_component(cls, **props):
        barter = props.pop("barter")
        return rx.cond(
            barter.bargainer_id == AuthState.user.id,
            rx.table.row(
                rx.table.cell(
                    barter.give, on_click=lambda: cls.mark_done(True)
                ),
                rx.table.cell(
                    barter.take, on_click=lambda: cls.mark_done(False)
                ),
            ),
            rx.table.row(
                rx.table.cell(
                    barter.take, on_click=lambda: cls.mark_done(False)
                ),
                rx.table.cell(
                    barter.give, on_click=lambda: cls.mark_done(True)
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
