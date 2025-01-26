from datetime import datetime, UTC

import reflex as rx
from sqlmodel import select

from .base import State, User
from give_and_take.models import Barter


class BarterState(State):
    give: str
    take: str
    bargainee: str
    success: int

    def create_barter(self) -> None:
        with rx.session() as session:
            self.success = 0
            if not self.give or not self.take or not self.bargainee:
                return rx.toast.error("All fields are required.")
            if not session.exec(
                select(User).where(User.username == self.bargainee)
            ).first():
                return rx.toast.error("Bargainee does not exist.")
            else:
                barter = Barter(
                    bargainer_id=self.user.id,
                    bargainee_id=session.exec(
                        select(User).where(User.username == self.bargainee)
                    )
                    .first()
                    .id,
                    give=self.give,
                    take=self.take,
                    created_at=datetime.now(UTC).isoformat(),
                )
                session.add(barter)
                session.commit()
                return rx.redirect("/")

    def attempt_barter(self) -> None:
        with rx.session() as session:
            self.success = 0
            if not self.give or not self.take or not self.bargainee:
                return rx.toast.error("All fields are required.")
            if not session.exec(
                select(User).where(User.username == self.bargainee)
            ).first():
                return rx.toast.error("Bargainee does not exist.")
        self.success = 1
