import json
from typing import Optional

import typer
from typing_extensions import Annotated

from readwise import get_document_by_id, get_documents

app = typer.Typer()


@app.command()
def list(location: str, n: Annotated[Optional[int], typer.Option("--number", "-n")] = None) -> None:
    """List documents.

    Params:
        location (str): The document's location, could be one of: new, later, shortlist, archive, feed
        n (Optional[int]): Limits the number of documents to a maximum (100 by default).

    Usage:
        $ readwise list new
    """
    documents = get_documents(location)[:n]
    fields_to_include = {"title", "id"}
    print(json.dumps([d.dict(include=fields_to_include) for d in documents], indent=2))


@app.command()
def get(id: str) -> None:
    """Get a single document from its ID.

    Usage:
        $ readwise get <document_id>
    """
    doc = get_document_by_id(id)
    if doc:
        print(doc.json(indent=2))
    else:
        print(f"No document with ID {id!r} could be found.")
