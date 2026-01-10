from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
from .models import CreateLinkRequest, Link
from .utils import check_url


def main():
    logger.info("Started cleaner bad links")
    clear_bad_links()


main()
app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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


@app.post("/create")
def create_click(request: CreateLinkRequest) -> Link:
    url = str(request.url)
    if not check_url(url):
        raise HTTPException(status_code=404, detail="Invalid URL")

    return existing if (existing := get_link_by_original_url(url)) else create_link(url)


@app.get("/{short_url}")
def click(short_url: str):
    link = get_link_by_short_url(short_url)

    if link:
        increment_link(link.id)
        return RedirectResponse(link.original_url, status_code=301)

    raise HTTPException(status_code=404, detail="Link not found")
