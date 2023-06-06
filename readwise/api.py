from os import environ
from typing import Final, Optional

import requests
from dotenv import load_dotenv

from readwise.model import Document, GetResponse

load_dotenv()
READWISE_TOKEN: Final[str] = environ["READWISE_TOKEN"]


def _make_get_request(params: dict[str, str]) -> GetResponse:
    json_data = requests.get(
        url="https://readwise.io/api/v3/list/",
        headers={"Authorization": f"Token {READWISE_TOKEN}"},
        params=params,
    ).json()

    return GetResponse(**json_data)


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
