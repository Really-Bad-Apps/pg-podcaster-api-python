# pg-podcaster-api-python

Python client library for the Podcast Guru podcaster portal REST API
(podcaster.podcastguru.io). Provides a synchronous client (`requests`) and an
asynchronous client (`httpx`) with one shared surface.

## Installation

```bash
pip install git+https://github.com/Really-Bad-Apps/pg-podcaster-api-python.git
```

### As a dependency in pyproject.toml
```toml
dependencies = [
    # TOKEN-FREE URL — never embed {env:CR_PAT} here.
    "pg-podcaster-api-python @ git+https://github.com/Really-Bad-Apps/pg-podcaster-api-python.git",
]
```

### As a dependency in requirements.txt
```
pg-podcaster-api-python @ git+https://github.com/Really-Bad-Apps/pg-podcaster-api-python.git
```

## Usage

```python
from pg_podcaster_api import PgPodcasterClient, AsyncPgPodcasterClient
from pg_podcaster_api.config import ClientConfig

config = ClientConfig(base_url="https://podcaster.podcastguru.io/api/v1", api_key="...")

with PgPodcasterClient(config) as client:
    print(client.health())

async def main() -> None:
    async with AsyncPgPodcasterClient(config) as client:
        print(await client.health())
```

Errors are raised as subclasses of `PgPodcasterError`; HTTP failures carry
`status_code` and the response `body`.

## Development

### Setup

> **Note (Python 3.13+):** `python3 -m venv .` writes a `.gitignore` with `*`
> into the venv root, which is the project root under this convention — so
> re-creating the venv here **overwrites this project's `.gitignore`**. If you
> re-create the venv later, restore the tracked file immediately:
> `git checkout .gitignore`.

```bash
python3 -m venv .
source bin/activate
pip install --upgrade -r requirements.txt
pip install -e .
pytest
```

## Conventions

- Every method on the sync client has an identical `async` twin.
- Request/response shapes come from `pg-podcaster-models`; no ad-hoc dicts once
  the backend defines real endpoints.
- Unix timestamps only, never `datetime`.

## License

MIT License

## Author

Jason Mazza
