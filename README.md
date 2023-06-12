![logo](https://github.com/floscha/readwise-api/raw/main/logo.png)

# Readwise API

An unofficial Python client for the [Readwise Reader API](https://readwise.io/reader_api).

## Installation

`pip install readwise-api`

## Usage

### Prerequisites

First, you have to obtain a [Readwise access token](https://readwise.io/access_token).
Then, the token has to be stored, either into an *.env* file or an environment variable using `export READWISE_TOKEN=<your_token>`.

### Python API

```python
import readwise
```

**List all documents:**

```python
readwise.get_documents(location="new")
```

**Get a single document by its ID:**

```python
readwise.get_document_by_id("<document_id>")
```

**Save a document to Readwise Reader**

```python
readwise.save_document("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

### CLI

**List all documents:**

```shell
readwise list new
```

Naturally, the output can be saved to a JSON file:

```shell
readwise list new > new_documents.json
```

**Get a single document by its ID:**

```shell
readwise get <document_id>
```

**Save a document to Readwise Reader**

```shell
readwise save "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
