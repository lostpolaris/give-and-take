import reflex as rx
from sqlmodel import select

from .base import State
from give_and_take.models import Barter, User


class HomeState(State):

    barter: [str, str]
    barters: list[Barter]

    def get_barters(self) -> list[Barter]:
        with rx.session() as session:
            barters =  session.exec(
                select(Barter).where(Barter.bargainer_id == self.user.id)
            )
            print(barters)
            return barters
