from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from crud import (
    create_link,
    get_link_by_id,
    get_link_by_original_url,
    get_link_by_short_url,
    increment_link,
)
from models import Link

app = FastAPI()


@app.get("/")
def main():
    return {"Hello": "World"}


@app.get("/click/{short_url}")
def click(short_url: str):
    link = get_link_by_short_url(short_url)

    if link:
        increment_link(link.id)
        return RedirectResponse(link.original_url, status_code=301)

    raise HTTPException(status_code=404, detail="Link not found")


@app.get("/click/info")
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


@app.post("/click/{originate_url}")
def create_click(originate_url: str) -> Link:
    link = create_link(originate_url)

    if link:
        return link

    raise HTTPException(status_code=404, detail="Link not found")
