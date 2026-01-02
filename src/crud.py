from sqlmodel import Session, delete, select

from database import engine
from models import Link
from utils import generate_short_url, nowtime


def create_link(original_url: str) -> Link:
    with Session(engine) as session:
        short_url = generate_short_url()

        link = Link(original_url=original_url, short_url=short_url)
        session.add(link)
        session.commit()
        session.refresh(link)

    return link


def get_link_by_id(link_id: int) -> Link | None:
    with Session(engine) as session:
        statement = select(Link).where(Link.id == link_id)
        link = session.exec(statement).first()

    return link


def get_link_by_short_url(short_url: str) -> Link | None:
    with Session(engine) as session:
        statement = select(Link).where(Link.short_url == short_url)
        link = session.exec(statement).first()

    return link


def get_link_by_original_url(original_url: str) -> Link | None:
    with Session(engine) as session:
        statement = select(Link).where(Link.original_url == original_url)
        link = session.exec(statement).first()

    return link


def increment_link(link_id: int) -> Link | None:
    with Session(engine) as session:
        statement = select(Link).where(Link.id == link_id)
        link = session.exec(statement).first()

        if link:
            link.clicks += 1
            session.refresh(link)
            session.commit()

        return link


def delete_link(link_id: int):
    with Session(engine) as session:
        statement = select(Link).where(Link.id == link_id)
        link = session.exec(statement).first()

        if link:
            session.delete(link)
            session.commit()


def delete_overdue_links():
    with Session(engine) as session:
        statement = delete(Link).where(
            Link.expires_at.is_not(None),  # type: ignore
            Link.expires_at < nowtime(),  # type: ignore
        )
        session.exec(statement).all()
        session.commit()
