import reflex as rx


class User(rx.Model, table=True):
    username: str
    password: str


class Barter(rx.Model, table=True):
    bargainer_id: int
    bargainee_id: int
    give: str
    take: str
    created_at: str


class Associations(rx.Model, table=True):
    bargainer: int
    bargainee: int
