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
        "title": "Entwicklerwerkzeuge Zustände",
        "url": "/config/developer-tools/state",
        "icon": "mdi:format-list-bulleted",
        "require_admin": True,
    },
    "service": {
        "title": "Entwicklerwerkzeuge Dienste",
        "url": "/config/developer-tools/service",
        "icon": "mdi:cog-play",
        "require_admin": True,
    },
    "template": {
        "title": "Entwicklerwerkzeuge Template",
        "url": "/config/developer-tools/template",
        "icon": "mdi:code-braces",
        "require_admin": True,
    },
    "event": {
        "title": "Entwicklerwerkzeuge Ereignisse",
        "url": "/config/developer-tools/event",
        "icon": "mdi:flash-outline",
        "require_admin": True,
    },
    "yaml": {
        "title": "Entwicklerwerkzeuge YAML",
        "url": "/config/developer-tools/yaml",
        "icon": "mdi:code-json",
        "require_admin": True,
    },
    "statistics": {
        "title": "Entwicklerwerkzeuge Statistiken",
        "url": "/config/developer-tools/statistics",
        "icon": "mdi:chart-bar",
        "require_admin": True,
    },
}
