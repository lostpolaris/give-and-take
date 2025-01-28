import asyncio

import reflex as rx
from sqlmodel import select

from .base import State
from give_and_take.models import Barter, User


class HomeState(State):

    barters: list[Barter]

    @rx.event()
    async def get_barters(self):
        with rx.session() as session:
            self.barters = session.exec(
                select(Barter).where(
                    (Barter.bargainer_id == self.user.id)
                    | (Barter.bargainee_id == self.user.id)
                )
            ).all()
