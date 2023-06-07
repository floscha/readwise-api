from os import environ
from time import sleep
from typing import Final, Optional

import requests
from dotenv import load_dotenv

from readwise.model import Document, GetResponse, PostRequest, PostResponse

load_dotenv()
READWISE_TOKEN: Final[str] = environ["READWISE_TOKEN"]
URL_BASE: Final[str] = "https://readwise.io/api/v3"


def _make_get_request(params: dict[str, str]) -> GetResponse:
    http_response = requests.get(
        url=f"{URL_BASE}/list/",
        headers={"Authorization": f"Token {READWISE_TOKEN}"},
        params=params,
    )
    if http_response.status_code != 429:
        return GetResponse(**http_response.json())

    # Respect rate limiting of maximum 20 requests per minute (https://readwise.io/reader_api).
    wait_time = int(http_response.headers["Retry-After"])
    sleep(wait_time)
    return _make_get_request(params)


def _make_post_request(payload: PostRequest) -> tuple[bool, PostResponse]:
    http_response = requests.post(
        url=f"{URL_BASE}/save/",
        headers={"Authorization": f"Token {READWISE_TOKEN}"},
        json=payload.dict(),
    )
    if http_response.status_code != 429:
        return (http_response.status_code == 200, PostResponse(**http_response.json()))

    # Respect rate limiting of maximum 20 requests per minute (https://readwise.io/reader_api).
    wait_time = int(http_response.headers["Retry-After"])
    sleep(wait_time)
    return _make_post_request(payload)


def get_documents(
    location: str,
    category: Optional[str] = None,
) -> list[Document]:
    """Get a list of documents from Readwise Reader.

    Params:
        location (str): The document's location, could be one of: new, later, shortlist, archive, feed
        category (str): The document's category, could be one of: article, email, rss, highlight, note, pdf, epub,
            tweet, video

    Returns:
        A list of `Document` objects.
    """
    params = {}
    if location not in ("new", "later", "shortlist", "archive", "feed"):
        raise ValueError(f"Parameter 'location' cannot be of value {location!r}")
    params["location"] = location
    if category:
        if category not in (
            "article",
            "email",
            "rss",
            "highlight",
            "note",
            "pdf",
            "epub",
            "tweet",
            "video",
        ):
            raise ValueError(f"Parameter 'category' cannot be of value {category!r}")
        params["category"] = category

    results: list[Document] = []
    while (response := _make_get_request(params)).next_page_cursor:
        results.extend(response.results)
        params["pageCursor"] = response.next_page_cursor
    else:
        # Make sure not to forget last response where `next_page_cursor` is None.
        results.extend(response.results)

    return results


def get_document_by_id(id: str) -> Document | None:
    """Get a single documents from Readwise Reader by its ID.

    Params:
        id (str): The document's unique id. Using this parameter it will return just one document, if found.

    Returns:
        A `Document` object if a document with the given ID exists, or None otherwise.
    """
    response = _make_get_request({"id": id})
    if response.count == 1:
        return response.results[0]
    else:
        return None


def save_document(url: str) -> tuple[bool, PostResponse]:
    """Save a document to Readwise Reader.

    Returns:
        int: Status code of 201 or 200 if document already exist.
        PostResponse: An object containing ID and Reader URL of the saved document.
    """
    return _make_post_request(PostRequest(url=url))
