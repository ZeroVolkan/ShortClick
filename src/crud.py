from typing import Sequence

from loguru import logger
from sqlmodel import Session, delete, select

from .database import engine
from .models import Link
from .utils import check_url, generate_short_url, nowtime


def create_link(original_url: str) -> Link:
    with Session(engine) as session:
        short_url = generate_short_url()

        link = Link(original_url=original_url, short_url=short_url)
        session.add(link)
        session.commit()
        session.refresh(link)

    logger.info(f"Created link {link.id} with short URL {link.short_url}")
    return link


def get_all_links() -> Sequence[Link]:
    with Session(engine) as session:
        statement = select(Link)
        links = session.exec(statement).all()

    logger.info(f"Retrieved {len(links)} links")
    return links


def get_link_by_id(link_id: int) -> Link | None:
    with Session(engine) as session:
        statement = select(Link).where(Link.id == link_id)
        link = session.exec(statement).first()

    if link is None:
        logger.error(f"Link with ID {link_id} not found")
    else:
        logger.info(f"Retrieved link {link.id} with short URL {link.short_url}")

    return link


def get_link_by_short_url(short_url: str) -> Link | None:
    with Session(engine) as session:
        statement = select(Link).where(Link.short_url == short_url)
        link = session.exec(statement).first()

    if link is None:
        logger.error(f"Link with short URL {short_url} not found")
    else:
        logger.info(f"Retrieved link {link.id} with short URL {link.short_url}")

    return link


def get_link_by_original_url(original_url: str) -> Link | None:
    with Session(engine) as session:
        statement = select(Link).where(Link.original_url == original_url)
        link = session.exec(statement).first()

    if link is None:
        logger.error(f"Link with original URL {original_url} not found")
    else:
        logger.info(f"Retrieved link {link.id} with short URL {link.short_url}")

    return link


def increment_link(link_id: int) -> Link | None:
    with Session(engine) as session:
        statement = select(Link).where(Link.id == link_id)
        link = session.exec(statement).first()

        if link:
            link.clicks += 1
            session.commit()
            logger.info(f"Incremented link {link.id} with short URL {link.short_url}")

    return link


def delete_link(link_id: int):
    with Session(engine) as session:
        statement = select(Link).where(Link.id == link_id)
        link = session.exec(statement).first()

        if link:
            session.delete(link)
            session.commit()
            logger.info(f"Deleted link {link.id} with short URL {link.short_url}")


def delete_overdue_links():
    with Session(engine) as session:
        statement = delete(Link).where(
            Link.expires_at.is_not(None),  # type: ignore
            Link.expires_at < nowtime(),  # type: ignore
        )
        session.exec(statement).all()
        session.commit()
        logger.info("Deleted overdue links")


def clear_bad_links():
    with Session(engine) as session:
        statement = select(Link)
        all = session.exec(statement).all()
        bad_links = [link for link in all if not check_url(link.original_url)]

        if not bad_links:
            logger.info("No bad links found")
            return

        for link in bad_links:
            session.delete(link)

        session.commit()
        logger.info(f"Deleted BAD links: {bad_links}")
