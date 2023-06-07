from typing import Any, Optional

from pydantic import BaseModel, Field


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
    next_page_cursor: Optional[str] = Field(..., alias="nextPageCursor")
    results: list[Document]


class PostRequest(BaseModel):
    """A POST request for the Readwise API to save documents to Reader.

    Fields:
        url (str): The document's unique URL. If you don't have one, you can provide a made up value such as
            https://yourapp.com#document1
        html (Optional[str]): The document's content, in valid html (see examples). If you don't provide this, we will
            try to scrape the URL you provided to fetch html from the open web.
        should_clean_html  (Optional[bool]): Only valid when html is provided. Pass true to have us automatically
            clean the html and parse the metadata (title/author) of the document for you. By default, this option is
            false.
        title (Optional[str]): The document's title, it will overwrite the original title of the document.
        author (Optional[str]): The document's author, it will overwrite the original author (if found during the
            parsing step).
        summary (Optional[str]): Summary of the document.
        published_date (Optional[str]): A datetime representing when the document was published in the ISO 8601
            format; default timezone is UTC. Example: "2020-07-14T20:11:24+00:00"
        image_url (Optional[str]): An image URL to use as cover image.
        location (Optional[str]): One of: new, later, archive or feed. Default is new.
            Represents the initial location of the document (previously called triage_status). Note: if you try to use
            a location the user doesn't have enabled in their settings, this value will be set to their default
            location.
        saved_using (Optional[str]): This value represents the source of the document
        tags (Optional[list[str]]): A list of strings containing tags, example: ["tag1", "tag2"]
    """

    url: str
    html: Optional[str] = None
    should_clean_html: Optional[bool] = None
    title: Optional[str] = None
    author: Optional[str] = None
    summary: Optional[str] = None
    published_date: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[str] = None
    saved_using: Optional[str] = None
    tags: Optional[list[str]] = None


class PostResponse(BaseModel):
    """A response from the Readwise API for POST requests.

    Fields:
        id (str): The ID of the saved document.
        url (str): The URL for the document in the Reader app.
    """

    id: str
    url: str
