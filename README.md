# Mattermost Python Client

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Mattermost API](https://img.shields.io/badge/Mattermost-API%20v4-0058CC?logo=mattermost&logoColor=white)](https://api.mattermost.com/)

A Python wrapper for the [Mattermost REST API v4](https://api.mattermost.com/), providing a clean and consistent interface for interacting with Mattermost servers.

## Features

- **Full API Coverage** — Users, Teams, Channels, Posts, Files, Webhooks, Bots, Reactions, Emoji
- **Type-Safe Models** — Dataclass-based models with `from_dict()` / `to_dict()` factory methods
- **Multiple Auth Methods** — Personal access token, session login (ID/password + MFA)
- **Flexible Configuration** — Direct values, environment variables, or `.env` file
- **Auto Pagination** — Built-in `get_all()` helpers that iterate through all pages
- **Rate Limit Handling** — Automatic retry with configurable delay
- **Context Manager** — `with` statement support for automatic resource cleanup
- **Detailed Exceptions** — Granular exception classes mapped to HTTP status codes

## Requirements

- Python 3.10+
- `requests >= 2.28.0`

## Installation

```bash
pip install requests
```

Clone or copy the `MattermostAPI/` package into your project.

## Quick Start

```python
from MattermostAPI import MattermostClient, MattermostConfig

config = MattermostConfig(
    url="https://mattermost.example.com",
    token="your-personal-access-token",
)

with MattermostClient(config) as client:
    me = client.users.get_me()
    print(f"Logged in as: {me.username}")

    client.posts.send_message("channel_id", "Hello from Python!")
```

---

## Configuration

### Direct Initialization

```python
config = MattermostConfig(
    url="https://mattermost.example.com",
    token="your-personal-access-token",
    timeout=30,
    verify_ssl=True,
    debug=False,
)
```

### From Environment Variables

```bash
export MM_URL=https://mattermost.example.com
export MM_TOKEN=your-token
```

```python
config = MattermostConfig.from_env()
```

### From `.env` File

```python
from pathlib import Path

config = MattermostConfig.from_env_file(Path(".env"))
```

### Configuration Options

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `url` | `str` | `""` | Mattermost server URL |
| `token` | `str` | `""` | Personal access token |
| `scheme` | `str` | `"https"` | URL scheme |
| `port` | `int` | `8065` | Server port |
| `timeout` | `int` | `30` | Request timeout (seconds) |
| `verify_ssl` | `bool` | `True` | Verify SSL certificates |
| `debug` | `bool` | `False` | Enable debug logging |
| `max_retries` | `int` | `3` | Max rate-limit retries |
| `retry_delay` | `float` | `1.0` | Delay between retries (seconds) |
| `login_id` | `str` | `None` | Login ID (for session auth) |
| `password` | `str` | `None` | Password (for session auth) |
| `mfa_token` | `str` | `None` | MFA token (for session auth) |

---

## Authentication

```python
# Token auth
config = MattermostConfig(url="https://...", token="your-token")
client = MattermostClient(config)

# Session login
config = MattermostConfig(url="https://...", login_id="admin@example.com", password="pass")
client = MattermostClient(config)
client.login()

# Logout
client.logout()
```

---

## API Endpoints

All endpoints are accessed via `MattermostClient` properties. For detailed method references and usage examples, see the **[Endpoints Documentation](Endpoints/README.md)**.

| Endpoint | Property | Description |
| --- | --- | --- |
| [Users](Endpoints/README.md#users--clientusers) | `client.users` | User retrieval, search, status, and profile management |
| [Teams](Endpoints/README.md#teams--clientteams) | `client.teams` | Team CRUD and member management |
| [Channels](Endpoints/README.md#channels--clientchannels) | `client.channels` | Channel CRUD, DM/group messaging, member management |
| [Posts](Endpoints/README.md#posts--clientposts) | `client.posts` | Message CRUD, threading, pinning |
| [Files](Endpoints/README.md#files--clientfiles) | `client.files` | File upload, download, metadata |
| [Webhooks](Endpoints/README.md#webhooks--clientwebhooks) | `client.webhooks` | Incoming/outgoing webhook CRUD and messaging |
| [Bots](Endpoints/README.md#bots--clientbots) | `client.bots` | Bot CRUD, enable/disable, icon management |
| [Reactions](Endpoints/README.md#reactions--clientreactions) | `client.reactions` | Post reaction add/remove/list |
| [Emoji](Endpoints/README.md#emoji--clientemoji) | `client.emoji` | Custom emoji CRUD and search |

---

## Error Handling

| Exception | Status | Description |
| --- | --- | --- |
| `MattermostApiError` | — | Base API error |
| `MattermostAuthenticationError` | 401 | Authentication failed |
| `MattermostForbiddenError` | 403 | Insufficient permissions |
| `MattermostNotFoundError` | 404 | Resource not found |
| `MattermostRateLimitError` | 429 | Rate limit exceeded |
| `MattermostConnectionError` | — | Connection failed |
| `MattermostTimeoutError` | — | Request timed out |
| `MattermostConfigError` | — | Configuration error |
| `MattermostFileError` | — | File handling error |

```python
from MattermostAPI.exceptions import MattermostApiError, MattermostNotFoundError

try:
    user = client.users.get_by_id("nonexistent-id")
except MattermostNotFoundError as e:
    print(f"Not found: {e.message}")
except MattermostApiError as e:
    print(f"API error [{e.status_code}]: {e.message}")
```

---

## Data Models

All API responses are deserialized into typed dataclass models:

| Model | Description |
| --- | --- |
| `User` / `UserStatus` | User account and online status |
| `Team` / `TeamMember` / `TeamStats` | Team, membership, and statistics |
| `Channel` / `ChannelMember` / `ChannelStats` | Channel, membership, and statistics |
| `Post` / `PostList` | Message and post collection |
| `FileInfo` / `FileUploadResponse` | File metadata and upload result |
| `IncomingWebhook` / `OutgoingWebhook` | Webhook configurations |
| `Bot` | Bot account |
| `Emoji` / `Reaction` | Custom emoji and post reactions |

All models provide:

- `from_dict(data)` — Create an instance from an API response dict
- `to_dict()` — Serialize to a dict
- `from_list(data_list)` — Create a list of instances from a list of dicts

---

## Project Structure

```shell
MattermostAPI/
├── __init__.py          # Package exports
├── client.py            # MattermostClient (main entry point)
├── config.py            # MattermostConfig (connection settings)
├── constants.py         # API constants and endpoint paths
├── exceptions.py        # Custom exception classes
├── http_client.py       # HTTP session and request handling
├── requirements.txt     # Dependencies
├── Endpoints/
│   ├── README.md        # Endpoint API reference
│   ├── base.py          # BaseEndpoint (pagination helpers)
│   ├── users.py         # UsersEndpoint
│   ├── teams.py         # TeamsEndpoint
│   ├── channels.py      # ChannelsEndpoint
│   ├── posts.py         # PostsEndpoint
│   ├── files.py         # FilesEndpoint
│   ├── webhooks.py      # WebhooksEndpoint
│   ├── bots.py          # BotsEndpoint
│   ├── reactions.py     # ReactionsEndpoint
│   └── emoji.py         # EmojiEndpoint
└── Models/
    ├── base.py           # BaseModel (dataclass base)
    ├── user.py           # User, UserStatus
    ├── team.py           # Team, TeamMember, TeamStats
    ├── channel.py        # Channel, ChannelMember, ChannelStats
    ├── post.py           # Post, PostList
    ├── file_info.py      # FileInfo, FileUploadResponse
    ├── webhook.py        # IncomingWebhook, OutgoingWebhook
    ├── bot.py            # Bot
    └── emoji.py          # Emoji, Reaction
```
