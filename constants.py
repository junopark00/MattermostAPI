"""
Mattermost API constants.

Defines API version, endpoint paths, pagination defaults, HTTP status codes,
and other magic numbers as named constants.
"""

# =============================================================================
# API Defaults
# =============================================================================
API_VERSION: str = "v4"
API_BASE_PATH: str = f"/api/{API_VERSION}"

# =============================================================================
# Authentication
# =============================================================================
AUTH_HEADER_KEY: str = "Authorization"
AUTH_BEARER_PREFIX: str = "Bearer"
AUTH_COOKIE_KEY: str = "MMAUTHTOKEN"
TOKEN_HEADER_KEY: str = "Token"

# =============================================================================
# Pagination Defaults
# =============================================================================
DEFAULT_PAGE: int = 0
DEFAULT_PER_PAGE: int = 60
MAX_PER_PAGE: int = 200

# =============================================================================
# HTTP Request Defaults
# =============================================================================
DEFAULT_TIMEOUT_SECONDS: int = 30
DEFAULT_CONTENT_TYPE: str = "application/json"
DEFAULT_SCHEME: str = "https"
DEFAULT_PORT: int = 8065

# =============================================================================
# HTTP Status Codes
# =============================================================================
HTTP_OK: int = 200
HTTP_CREATED: int = 201
HTTP_NO_CONTENT: int = 204
HTTP_BAD_REQUEST: int = 400
HTTP_UNAUTHORIZED: int = 401
HTTP_FORBIDDEN: int = 403
HTTP_NOT_FOUND: int = 404
HTTP_TOO_MANY_REQUESTS: int = 429
HTTP_INTERNAL_SERVER_ERROR: int = 500

# =============================================================================
# Rate Limit Headers
# =============================================================================
RATE_LIMIT_HEADER: str = "X-Ratelimit-Limit"
RATE_LIMIT_REMAINING_HEADER: str = "X-Ratelimit-Remaining"
RATE_LIMIT_RESET_HEADER: str = "X-Ratelimit-Reset"

# =============================================================================
# Rate Limit Retry Settings
# =============================================================================
RATE_LIMIT_MAX_RETRIES: int = 3
RATE_LIMIT_RETRY_DELAY_SECONDS: float = 1.0

# =============================================================================
# Channel Types
# =============================================================================
CHANNEL_TYPE_OPEN: str = "O"
CHANNEL_TYPE_PRIVATE: str = "P"
CHANNEL_TYPE_DIRECT: str = "D"
CHANNEL_TYPE_GROUP: str = "G"

# =============================================================================
# Team Types
# =============================================================================
TEAM_TYPE_OPEN: str = "O"
TEAM_TYPE_INVITE: str = "I"

# =============================================================================
# User Status
# =============================================================================
STATUS_ONLINE: str = "online"
STATUS_AWAY: str = "away"
STATUS_DND: str = "dnd"
STATUS_OFFLINE: str = "offline"

# =============================================================================
# Special Identifiers
# =============================================================================
ME: str = "me"

# =============================================================================
# Endpoint Path Templates
# =============================================================================

# Users
ENDPOINT_USERS: str = "/users"
ENDPOINT_USERS_LOGIN: str = "/users/login"
ENDPOINT_USERS_LOGOUT: str = "/users/logout"
ENDPOINT_USER_BY_ID: str = "/users/{user_id}"
ENDPOINT_USER_BY_USERNAME: str = "/users/username/{username}"
ENDPOINT_USER_BY_EMAIL: str = "/users/email/{email}"
ENDPOINT_USERS_IDS: str = "/users/ids"
ENDPOINT_USERS_SEARCH: str = "/users/search"
ENDPOINT_USERS_AUTOCOMPLETE: str = "/users/autocomplete"
ENDPOINT_USER_IMAGE: str = "/users/{user_id}/image"
ENDPOINT_USER_TEAMS: str = "/users/{user_id}/teams"
ENDPOINT_USER_CHANNELS: str = "/users/{user_id}/teams/{team_id}/channels"

# Teams
ENDPOINT_TEAMS: str = "/teams"
ENDPOINT_TEAM_BY_ID: str = "/teams/{team_id}"
ENDPOINT_TEAM_BY_NAME: str = "/teams/name/{name}"
ENDPOINT_TEAM_MEMBERS: str = "/teams/{team_id}/members"
ENDPOINT_TEAM_MEMBER: str = "/teams/{team_id}/members/{user_id}"
ENDPOINT_TEAM_MEMBERS_IDS: str = "/teams/{team_id}/members/ids"
ENDPOINT_TEAM_STATS: str = "/teams/{team_id}/stats"
ENDPOINT_TEAMS_SEARCH: str = "/teams/search"

# Channels
ENDPOINT_CHANNELS: str = "/channels"
ENDPOINT_CHANNEL_BY_ID: str = "/channels/{channel_id}"
ENDPOINT_CHANNELS_DIRECT: str = "/channels/direct"
ENDPOINT_CHANNELS_GROUP: str = "/channels/group"
ENDPOINT_TEAM_CHANNELS: str = "/teams/{team_id}/channels"
ENDPOINT_TEAM_CHANNELS_SEARCH: str = "/teams/{team_id}/channels/search"
ENDPOINT_TEAM_CHANNEL_BY_NAME: str = "/teams/{team_id}/channels/name/{channel_name}"
ENDPOINT_CHANNEL_MEMBERS: str = "/channels/{channel_id}/members"
ENDPOINT_CHANNEL_MEMBER: str = "/channels/{channel_id}/members/{user_id}"
ENDPOINT_CHANNEL_STATS: str = "/channels/{channel_id}/stats"

# Posts
ENDPOINT_POSTS: str = "/posts"
ENDPOINT_POST_BY_ID: str = "/posts/{post_id}"
ENDPOINT_CHANNEL_POSTS: str = "/channels/{channel_id}/posts"
ENDPOINT_POST_THREAD: str = "/posts/{post_id}/thread"
ENDPOINT_POST_PIN: str = "/posts/{post_id}/pin"
ENDPOINT_POST_UNPIN: str = "/posts/{post_id}/unpin"
ENDPOINT_POSTS_SEARCH: str = "/teams/{team_id}/posts/search"

# Files
ENDPOINT_FILES: str = "/files"
ENDPOINT_FILE_BY_ID: str = "/files/{file_id}"
ENDPOINT_FILE_THUMBNAIL: str = "/files/{file_id}/thumbnail"
ENDPOINT_FILE_PREVIEW: str = "/files/{file_id}/preview"
ENDPOINT_FILE_LINK: str = "/files/{file_id}/link"
ENDPOINT_FILE_INFO: str = "/files/{file_id}/info"

# Webhooks
ENDPOINT_HOOKS_INCOMING: str = "/hooks/incoming"
ENDPOINT_HOOK_INCOMING_BY_ID: str = "/hooks/incoming/{hook_id}"
ENDPOINT_HOOKS_OUTGOING: str = "/hooks/outgoing"
ENDPOINT_HOOK_OUTGOING_BY_ID: str = "/hooks/outgoing/{hook_id}"
ENDPOINT_HOOK_OUTGOING_REGEN_TOKEN: str = "/hooks/outgoing/{hook_id}/regen_token"

# Bots
ENDPOINT_BOTS: str = "/bots"
ENDPOINT_BOT_BY_ID: str = "/bots/{bot_user_id}"
ENDPOINT_BOT_DISABLE: str = "/bots/{bot_user_id}/disable"
ENDPOINT_BOT_ENABLE: str = "/bots/{bot_user_id}/enable"
ENDPOINT_BOT_ASSIGN: str = "/bots/{bot_user_id}/assign/{user_id}"
ENDPOINT_BOT_ICON: str = "/bots/{bot_user_id}/icon"

# Reactions
ENDPOINT_REACTIONS: str = "/reactions"
ENDPOINT_POST_REACTIONS: str = "/posts/{post_id}/reactions"

# Status
ENDPOINT_USER_STATUS: str = "/users/{user_id}/status"
ENDPOINT_USERS_STATUS_IDS: str = "/users/status/ids"

# Emoji
ENDPOINT_EMOJI: str = "/emoji"
ENDPOINT_EMOJI_BY_ID: str = "/emoji/{emoji_id}"
ENDPOINT_EMOJI_BY_NAME: str = "/emoji/name/{emoji_name}"
ENDPOINT_EMOJI_IMAGE: str = "/emoji/{emoji_id}/image"
ENDPOINT_EMOJI_SEARCH: str = "/emoji/search"

# WebSocket
ENDPOINT_WEBSOCKET: str = f"/api/{API_VERSION}/websocket"
