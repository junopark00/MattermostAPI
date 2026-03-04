# Endpoints API Reference

Detailed method references and usage examples for all `MattermostClient` endpoints.

> **Back to [Main Documentation](../README.md)**

All examples assume a configured client:

```python
from MattermostAPI import MattermostClient, MattermostConfig

config = MattermostConfig(
    url="https://mattermost.example.com",
    token="your-personal-access-token",
)
client = MattermostClient(config)
```

---

## Table of Contents

- [Users](#users--clientusers)
- [Teams](#teams--clientteams)
- [Channels](#channels--clientchannels)
- [Posts](#posts--clientposts)
- [Files](#files--clientfiles)
- [Webhooks](#webhooks--clientwebhooks)
- [Bots](#bots--clientbots)
- [Reactions](#reactions--clientreactions)
- [Emoji](#emoji--clientemoji)

---

## Users — `client.users`

User retrieval, search, status, and profile management.

| Method | Description | Returns |
| --- | --- | --- |
| `get_me()` | Get the authenticated user | `User` |
| `get_by_id(user_id)` | Get a user by ID | `User` |
| `get_by_username(username)` | Get a user by username | `User` |
| `get_by_email(email)` | Get a user by email | `User` |
| `get_list(page, per_page, in_team, in_channel)` | List users (paginated) | `list[User]` |
| `get_all(in_team, in_channel)` | Get all users (auto-pagination) | `list[User]` |
| `get_by_ids(user_ids)` | Bulk-fetch users by IDs | `list[User]` |
| `search(term, **kwargs)` | Search users | `list[User]` |
| `autocomplete(name, team_id, channel_id)` | Autocomplete user search | `list[User]` |
| `create(username, email, password, **kwargs)` | Create a new user | `User` |
| `update(user_id, **kwargs)` | Update user info | `User` |
| `deactivate(user_id)` | Deactivate a user | `bool` |
| `get_status(user_id)` | Get user status | `UserStatus` |
| `update_status(user_id, status)` | Update user status | `UserStatus` |
| `get_statuses_by_ids(user_ids)` | Bulk-fetch user statuses | `list[UserStatus]` |
| `get_teams(user_id)` | Get user's teams | `list[dict]` |
| `get_channels_for_team(user_id, team_id)` | Get user's channels in a team | `list[dict]` |

### Users Examples

```python
# Get current user
me = client.users.get_me()
print(f"{me.username} ({me.email})")

# Find a user by username
user = client.users.get_by_username("john.doe")

# Search users
results = client.users.search("john")
for u in results:
    print(f"  {u.username} - {u.email}")

# List all users in a team
all_users = client.users.get_all(in_team="team_id")

# Bulk-fetch by IDs
users = client.users.get_by_ids(["id1", "id2", "id3"])

# Update user status
client.users.update_status(me.id, "dnd")  # online | away | dnd | offline

# Get user's teams and channels
teams = client.users.get_teams(me.id)
channels = client.users.get_channels_for_team(me.id, "team_id")
```

---

## Teams — `client.teams`

Team CRUD and member management.

| Method | Description | Returns |
| --- | --- | --- |
| `get_by_id(team_id)` | Get a team by ID | `Team` |
| `get_by_name(name)` | Get a team by name (slug) | `Team` |
| `get_list(page, per_page)` | List teams (paginated) | `list[Team]` |
| `get_all()` | Get all teams (auto-pagination) | `list[Team]` |
| `search(term)` | Search teams by name | `list[Team]` |
| `create(name, display_name, team_type, **kwargs)` | Create a team | `Team` |
| `update(team_id, **kwargs)` | Update team info | `Team` |
| `delete(team_id)` | Soft-delete a team | `bool` |
| `get_members(team_id, page, per_page)` | List team members | `list[TeamMember]` |
| `add_member(team_id, user_id)` | Add a member to a team | `TeamMember` |
| `remove_member(team_id, user_id)` | Remove a member from a team | `bool` |
| `get_members_by_ids(team_id, user_ids)` | Bulk-fetch team members | `list[TeamMember]` |
| `get_stats(team_id)` | Get team statistics | `TeamStats` |

### Teams Examples

```python
# List all teams
teams = client.teams.get_all()
for t in teams:
    print(f"{t.display_name} ({t.name})")

# Get a team by name
team = client.teams.get_by_name("developers")

# Create a team
team = client.teams.create(
    name="dev-team",
    display_name="Development Team",
    team_type="O",  # 'O' = Open, 'I' = Invite-only
)

# Member management
client.teams.add_member(team.id, user.id)
client.teams.remove_member(team.id, user.id)

# Get team members and stats
members = client.teams.get_members(team.id)
stats = client.teams.get_stats(team.id)
print(f"Total members: {stats.total_member_count}")
```

---

## Channels — `client.channels`

Channel CRUD, direct/group messaging, and member management.

### Channels Methods

| Method | Description | Returns |
| --- | --- | --- |
| `get_by_id(channel_id)` | Get a channel by ID | `Channel` |
| `get_by_name(team_id, channel_name)` | Get a channel by team ID and name | `Channel` |
| `get_list_for_team(team_id, page, per_page)` | List channels in a team | `list[Channel]` |
| `search_in_team(team_id, term)` | Search channels in a team | `list[Channel]` |
| `create(team_id, name, display_name, channel_type, **kwargs)` | Create a channel | `Channel` |
| `update(channel_id, **kwargs)` | Update channel info | `Channel` |
| `delete(channel_id)` | Delete (archive) a channel | `bool` |
| `create_direct(user_id_1, user_id_2)` | Create/get a 1:1 DM channel | `Channel` |
| `create_group(user_ids)` | Create a group message channel | `Channel` |
| `get_members(channel_id, page, per_page)` | List channel members | `list[ChannelMember]` |
| `add_member(channel_id, user_id)` | Add a member to a channel | `ChannelMember` |
| `remove_member(channel_id, user_id)` | Remove a member from a channel | `bool` |
| `get_stats(channel_id)` | Get channel statistics | `ChannelStats` |

### Channels Examples

```python
# List channels in a team
channels = client.channels.get_list_for_team(team.id)
for ch in channels:
    print(f"#{ch.display_name} (type: {ch.type})")

# Get a channel by name
general = client.channels.get_by_name(team.id, "general")

# Create a public channel
channel = client.channels.create(
    team_id=team.id,
    name="announcements",
    display_name="Announcements",
    channel_type="O",  # 'O' = Open, 'P' = Private
    purpose="Company-wide announcements",
    header="📢 Read-only for most users",
)

# Create a 1:1 DM channel
me = client.users.get_me()
dm = client.channels.create_direct(me.id, other_user.id)
client.posts.send_message(dm.id, "Hello! 👋")

# Create a group message channel (3+ users)
group = client.channels.create_group(["user_id_1", "user_id_2", "user_id_3"])

# Member management
client.channels.add_member(channel.id, user.id)
client.channels.remove_member(channel.id, user.id)

# Channel stats
stats = client.channels.get_stats(channel.id)
print(f"Members: {stats.member_count}")
```

---

## Posts — `client.posts`

Message CRUD, threading, pinning, and search.

| Method | Description | Returns |
| --- | --- | --- |
| `get_by_id(post_id)` | Get a post by ID | `Post` |
| `get_for_channel(channel_id, page, per_page, since, before, after)` | List posts in a channel | `PostList` |
| `get_thread(post_id)` | Get a post's thread (including replies) | `PostList` |
| `search(team_id, terms, **kwargs)` | Search posts in a team | `PostList` |
| `create(channel_id, message, root_id, file_ids, props)` | Create a post | `Post` |
| `update(post_id, message, **kwargs)` | Update a post | `Post` |
| `delete(post_id)` | Delete a post | `bool` |
| `pin(post_id)` | Pin a post to the channel | `bool` |
| `unpin(post_id)` | Unpin a post | `bool` |
| `send_message(channel_id, message, **kwargs)` | Send a message (alias for `create`) | `Post` |
| `send_reply(channel_id, root_id, message, **kwargs)` | Send a threaded reply | `Post` |

### Posts Examples

```python
# Send a simple message
post = client.posts.send_message(channel_id, "Hello! 🎉")

# Send a threaded reply
reply = client.posts.send_reply(channel_id, post.id, "This is a reply 📝")

# Send a rich message with attachments
client.posts.create(
    channel_id=channel_id,
    message="## 📊 Daily Report",
    props={
        "attachments": [
            {
                "color": "#36a64f",
                "title": "Build Status",
                "text": "All builds passed.",
                "fields": [
                    {"short": True, "title": "Env", "value": "Production"},
                    {"short": True, "title": "Version", "value": "v2.1.0"},
                    {"short": False, "title": "Changes", "value": "- Bug fixes\n- Performance improvements"},
                ],
            }
        ]
    },
)

# Send a message with file attachments
post = client.posts.create(
    channel_id=channel_id,
    message="📎 File attached.",
    file_ids=["file_id_1", "file_id_2"],
)

# Read channel posts
post_list = client.posts.get_for_channel(channel_id)
for p in post_list.get_posts():
    print(f"[{p.user_id}] {p.message}")

# Get a thread
thread = client.posts.get_thread(post.id)

# Search posts
results = client.posts.search(team.id, "deployment")

# Pin / Unpin
client.posts.pin(post.id)
client.posts.unpin(post.id)

# Edit a post
client.posts.update(post.id, "Updated message")

# Delete a post
client.posts.delete(post.id)
```

---

## Files — `client.files`

File upload, download, metadata, and previews.

| Method | Description | Returns |
| --- | --- | --- |
| `upload(channel_id, file_path)` | Upload a file to a channel | `FileUploadResponse` |
| `get_info(file_id)` | Get file metadata | `FileInfo` |
| `get_content(file_id)` | Get raw file binary data | `bytes` |
| `download(file_id, save_path)` | Download a file to local storage | `Path` |
| `get_thumbnail(file_id, save_path)` | Download file thumbnail (images) | `Path` |
| `get_preview(file_id, save_path)` | Download file preview | `Path` |
| `get_public_link(file_id)` | Get a public sharing link | `str` |

### Files Examples

```python
from pathlib import Path

# Upload a file and attach to a message
upload = client.files.upload(channel_id, Path("report.pdf"))
file_ids = upload.get_file_ids()

client.posts.create(
    channel_id=channel_id,
    message="📎 Report attached.",
    file_ids=file_ids,
)

# Get file info
info = client.files.get_info(file_ids[0])
print(f"{info.name} ({info.size} bytes, {info.mime_type})")

# Download a file
saved = client.files.download("file_id", Path("./downloads/report.pdf"))
print(f"Saved to: {saved}")

# Download thumbnail / preview
client.files.get_thumbnail("file_id", Path("./thumb.jpg"))
client.files.get_preview("file_id", Path("./preview.jpg"))

# Get public link
link = client.files.get_public_link("file_id")
print(f"Public URL: {link}")
```

---

## Webhooks — `client.webhooks`

Incoming and outgoing webhook CRUD and messaging.

### Incoming Webhook Methods

| Method | Description | Returns |
| --- | --- | --- |
| `create_incoming(channel_id, display_name, description, username, icon_url)` | Create an incoming webhook | `IncomingWebhook` |
| `get_incoming_list(page, per_page, team_id)` | List incoming webhooks | `list[IncomingWebhook]` |
| `get_incoming_by_id(hook_id)` | Get an incoming webhook | `IncomingWebhook` |
| `update_incoming(hook_id, **kwargs)` | Update an incoming webhook | `IncomingWebhook` |
| `delete_incoming(hook_id)` | Delete an incoming webhook | `bool` |
| `send_to_incoming(webhook_url, text, channel, username, icon_url, attachments, props)` | Send a message via webhook URL | `bool` |

### Outgoing Webhook Methods

| Method | Description | Returns |
| --- | --- | --- |
| `create_outgoing(team_id, display_name, description, channel_id, trigger_words, callback_urls, trigger_when, content_type)` | Create an outgoing webhook | `OutgoingWebhook` |
| `get_outgoing_list(page, per_page, team_id)` | List outgoing webhooks | `list[OutgoingWebhook]` |
| `get_outgoing_by_id(hook_id)` | Get an outgoing webhook | `OutgoingWebhook` |
| `update_outgoing(hook_id, **kwargs)` | Update an outgoing webhook | `OutgoingWebhook` |
| `delete_outgoing(hook_id)` | Delete an outgoing webhook | `bool` |
| `regenerate_outgoing_token(hook_id)` | Regenerate webhook token | `OutgoingWebhook` |

### Webhooks Examples

```python
# Create an incoming webhook
hook = client.webhooks.create_incoming(
    channel_id=channel_id,
    display_name="Alert Bot",
    description="Sends deployment alerts",
)

# List incoming webhooks
hooks = client.webhooks.get_incoming_list(team_id=team.id)

# Send a simple message via webhook URL
client.webhooks.send_to_incoming(
    webhook_url="https://mattermost.example.com/hooks/your-hook-id",
    text="🚀 New deployment completed!",
)

# Send a rich message via webhook
client.webhooks.send_to_incoming(
    webhook_url="https://mattermost.example.com/hooks/your-hook-id",
    text="Build result notification",
    username="CI Bot",
    icon_url="https://example.com/ci-icon.png",
    attachments=[
        {
            "color": "#00FF00",
            "title": "✅ Build Succeeded",
            "text": "Main branch build succeeded.",
            "fields": [
                {"short": True, "title": "Branch", "value": "main"},
                {"short": True, "title": "Duration", "value": "3m 42s"},
            ],
        }
    ],
)

# Create an outgoing webhook
outgoing = client.webhooks.create_outgoing(
    team_id=team.id,
    display_name="Command Bot",
    trigger_words=["!deploy", "!status"],
    callback_urls=["https://your-server.com/webhook"],
)

# Regenerate token
client.webhooks.regenerate_outgoing_token(outgoing.id)
```

---

## Bots — `client.bots`

Bot CRUD, enable/disable, and icon management.

| Method | Description | Returns |
| --- | --- | --- |
| `create(username, display_name, description)` | Create a bot | `Bot` |
| `get_list(page, per_page, include_deleted)` | List bots | `list[Bot]` |
| `get_by_id(bot_user_id)` | Get a bot by user ID | `Bot` |
| `update(bot_user_id, **kwargs)` | Update a bot | `Bot` |
| `disable(bot_user_id)` | Disable a bot | `Bot` |
| `enable(bot_user_id)` | Enable a bot | `Bot` |
| `assign_to_user(bot_user_id, user_id)` | Reassign bot ownership | `Bot` |
| `set_icon(bot_user_id, icon_path)` | Set bot icon image | `bool` |
| `delete_icon(bot_user_id)` | Delete bot icon | `bool` |

### Bots Examples

```python
from pathlib import Path

# Create a bot
bot = client.bots.create(
    username="alert-bot",
    display_name="Alert Bot",
    description="Sends automated alerts",
)

# List all bots (including deleted)
bots = client.bots.get_list(include_deleted=True)

# Update bot info
client.bots.update(bot.user_id, display_name="New Name")

# Disable / Enable
client.bots.disable(bot.user_id)
client.bots.enable(bot.user_id)

# Set bot icon
client.bots.set_icon(bot.user_id, Path("bot_icon.png"))

# Reassign ownership
client.bots.assign_to_user(bot.user_id, new_owner_id)
```

---

## Reactions — `client.reactions`

Post reaction (emoji) add, remove, and list.

| Method | Description | Returns |
| --- | --- | --- |
| `add(user_id, post_id, emoji_name)` | Add a reaction to a post | `Reaction` |
| `remove(user_id, post_id, emoji_name)` | Remove a reaction from a post | `bool` |
| `get_for_post(post_id)` | Get all reactions for a post | `list[Reaction]` |

### Reactions Examples

```python
me = client.users.get_me()

# Add reactions
client.reactions.add(me.id, post.id, "thumbsup")
client.reactions.add(me.id, post.id, "heart")

# List all reactions on a post
reactions = client.reactions.get_for_post(post.id)
for r in reactions:
    print(f":{r.emoji_name}: by {r.user_id}")

# Remove a reaction
client.reactions.remove(me.id, post.id, "thumbsup")
```

---

## Emoji — `client.emoji`

Custom emoji CRUD and search.

| Method | Description | Returns |
| --- | --- | --- |
| `get_list(page, per_page)` | List custom emoji (paginated) | `list[Emoji]` |
| `get_by_id(emoji_id)` | Get a custom emoji by ID | `Emoji` |
| `get_by_name(emoji_name)` | Get a custom emoji by name (without colons) | `Emoji` |
| `search(term, prefix_only)` | Search custom emoji | `list[Emoji]` |
| `create(name, image_path)` | Create a custom emoji | `Emoji` |
| `delete(emoji_id)` | Delete a custom emoji | `bool` |
| `get_image(emoji_id, save_path)` | Download emoji image | `Path` |

### Emoji Examples

```python
from pathlib import Path

# List all custom emoji
emojis = client.emoji.get_list()
for e in emojis:
    print(f":{e.name}: (id: {e.id})")

# Search emoji
results = client.emoji.search("party")

# Create a custom emoji
emoji = client.emoji.create("party_parrot", Path("party_parrot.gif"))

# Download emoji image
client.emoji.get_image(emoji.id, Path("./downloaded_emoji.gif"))

# Delete
client.emoji.delete(emoji.id)
```
