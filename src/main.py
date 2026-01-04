from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from .crud import (
    clear_bad_links,
    create_link,
    get_all_links,
    get_link_by_id,
    get_link_by_original_url,
    get_link_by_short_url,
    increment_link,
)
from .logger import logger
from .models import Link
from .utils import check_url


def main():
    """Generaly work"""
    logger.info("Started cleaner bad links")
    clear_bad_links()


main()
app = FastAPI()


@app.get("/")
def index():
    return get_all_links()


@app.get("/{short_url}")
def click(short_url: str):
    link = get_link_by_short_url(short_url)

    if link:
        increment_link(link.id)
        return RedirectResponse(link.original_url, status_code=301)

    raise HTTPException(status_code=404, detail="Link not found")


@app.get("/info")
def info(
    link_id: int | None = None,
    short_url: str | None = None,
    original_url: str | None = None,
) -> Link | None:
    if link_id:
        return get_link_by_id(link_id)
    if short_url:
        return get_link_by_short_url(short_url)
    if original_url:
        return get_link_by_original_url(original_url)
    raise HTTPException(status_code=404, detail="Link not found")


@app.post("/create/{originate_url}")
def create_click(originate_url: str) -> Link:
    if not check_url(originate_url):
        raise HTTPException(status_code=404, detail="Invalid URL")

    return (
        existing
        if (existing := get_link_by_original_url(originate_url))
        else create_link(originate_url)
    )
