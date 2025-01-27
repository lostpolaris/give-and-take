import reflex as rx


class User(rx.Model, table=True):
    username: str
    password: str


class Barter(rx.Model, table=True):
    bargainer_id: int
    bargainee_id: int
    give: str
    give_done: bool = False
    take: str
    take_done: bool = False
    created_at: str


class Associations(rx.Model, table=True):
    bargainer: int
    bargainee: int
