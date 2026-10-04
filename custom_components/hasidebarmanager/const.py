DOMAIN = "hasidebarmanager"

CONF_TAB_TITLE = "tab_title"
CONF_URL = "url"
CONF_ICON = "icon"
CONF_REQUIRE_ADMIN = "require_admin"
CONF_TEMPLATE_GROUP = "template_group"
CONF_TEMPLATE_ITEM = "template_item"

DEFAULT_ICON = "mdi:link"
DEFAULT_REQUIRE_ADMIN = True

TEMPLATE_GROUP_CUSTOM = "custom"
TEMPLATE_GROUP_DEVTOOLS = "developer_tools"

DEVTOOLS_TEMPLATES = {
    "state": {
        "url": "/config/developer-tools/state",
        "icon": "mdi:format-list-bulleted",
        "require_admin": True,
    },
    "service": {
        "url": "/config/developer-tools/service",
        "icon": "mdi:cog-play",
        "require_admin": True,
    },
    "template": {
        "url": "/config/developer-tools/template",
        "icon": "mdi:code-braces",
        "require_admin": True,
    },
    "event": {
        "url": "/config/developer-tools/event",
        "icon": "mdi:flash-outline",
        "require_admin": True,
    },
    "yaml": {
        "url": "/config/developer-tools/yaml",
        "icon": "mdi:code-json",
        "require_admin": True,
    },
    "statistics": {
        "url": "/config/developer-tools/statistics",
        "icon": "mdi:chart-bar",
        "require_admin": True,
    },
}
