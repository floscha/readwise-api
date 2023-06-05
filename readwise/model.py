from typing import Any, Optional

from pydantic import BaseModel


class Tag(BaseModel):
    """A tag used to organize documents in Readwise Reader."""

    name: str
    type: str
    created: int


class Document(BaseModel):
    """A single document saved in the Readwise Reader."""

    id: str
    url: str
    title: str
    author: str
    source: Optional[str]
    category: str
    location: str
    tags: Optional[dict[str, Tag]]
    site_name: Optional[str]
    word_count: Optional[int]
    created_at: str
    updated_at: str
    published_date: Optional[str]
    summary: Optional[str]
    image_url: Optional[str]
    content: Any
    source_url: str


class GetResponse(BaseModel):
    """A response from the Readwise API for GET requests.

    Fields:
        count (int): The number of returned documents (max 100).
        next_page_cursor (Optional[str]): If there are more the 100 documents, a `next_page_cursor` is added to the
            response, which can be passed as a starting point for an additional request.
        results (list[Document]): The list of documents from Readwise.
    """

    count: int
    next_page_cursor: Optional[str]
    results: list[Document]
