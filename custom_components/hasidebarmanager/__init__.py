from __future__ import annotations

import asyncio
import logging
from functools import partial
from pathlib import Path

from homeassistant.components.frontend import (
    async_register_built_in_panel,
    async_remove_panel,
)
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_ICON,
    CONF_REQUIRE_ADMIN,
    CONF_TAB_TITLE,
    CONF_URL,
    DEFAULT_ICON,
    DEFAULT_REQUIRE_ADMIN,
    DOMAIN,
)

LOGGER = logging.getLogger(__name__)

REDIRECT_JS_FILENAME = "ha-sidebar-manager-redirect.js"
REDIRECT_JS_URL = f"/local/{REDIRECT_JS_FILENAME}"

_FLAG_KEY = f"{DOMAIN}_js_registered"
_LOCK_KEY = f"{DOMAIN}_js_register_lock"

REDIRECT_JS = """\
class HASidebarManagerRedirect extends HTMLElement {
  constructor() {
    super();
    this._target = null;
  }

  set panel(info) {
    this._target = info?.config?.target ?? null;
    this._redirect();
  }

  connectedCallback() {
    this._redirect();
  }

  _redirect() {
    const target = this._target;
    if (!target) {
      this.innerHTML = "<p style='padding:1em;font-family:sans-serif'>Keine Ziel-URL konfiguriert.</p>";
      return;
    }

    requestAnimationFrame(() => {
      if (window.history?.replaceState) {
        window.history.replaceState(null, "", target);
        window.dispatchEvent(
          new CustomEvent("location-changed", { detail: { replace: true } })
        );
      } else {
        window.location.href = target;
      }
    });
  }
}

if (!customElements.get("ha-sidebar-manager-redirect")) {
  customElements.define("ha-sidebar-manager-redirect", HASidebarManagerRedirect);
}
""".strip()


def _js_path(hass: HomeAssistant) -> Path:
    return Path(hass.config.path("www", REDIRECT_JS_FILENAME))


async def _ensure_redirect_js(hass: HomeAssistant) -> str:
    """Write the redirect JS file only if content changed."""
    js_path = _js_path(hass)

    await hass.async_add_executor_job(
        partial(js_path.parent.mkdir, parents=True, exist_ok=True)
    )

    current_content = None
    if js_path.exists():
        try:
            current_content = await hass.async_add_executor_job(
                partial(js_path.read_text, encoding="utf-8")
            )
        except Exception:
            current_content = None

    if current_content != REDIRECT_JS:
        await hass.async_add_executor_job(
            partial(js_path.write_text, REDIRECT_JS, encoding="utf-8")
        )

    return str(js_path)


async def _register_redirect_resource(hass: HomeAssistant) -> None:
    """Register the redirect JS as a static resource exactly once per HA run.

    Home Assistant 2026.6 rejects duplicate GET route registrations.
    Multiple config entries can race during startup, so we guard registration
    with a shared asyncio.Lock stored in hass.data.
    """
    if hass.data.get(_FLAG_KEY):
        return

    lock: asyncio.Lock = hass.data.setdefault(_LOCK_KEY, asyncio.Lock())

    async with lock:
        if hass.data.get(_FLAG_KEY):
            return

        js_path = await _ensure_redirect_js(hass)

        try:
            await hass.http.async_register_static_paths(
                [
                    StaticPathConfig(
                        REDIRECT_JS_URL,
                        js_path,
                        cache_headers=False,
                    )
                ]
            )
        except RuntimeError as exc:
            msg = str(exc)
            if "already registered" not in msg and "will never be executed" not in msg:
                raise
            LOGGER.debug("Static path already registered, reusing existing route: %s", msg)

        hass.data[_FLAG_KEY] = True


def _panel_name(entry: ConfigEntry) -> str:
    return f"{DOMAIN}_{entry.entry_id[:8]}"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HA Sidebar Manager from a config entry."""
    tab_title: str = entry.data[CONF_TAB_TITLE]
    url: str = entry.data[CONF_URL]
    icon: str = entry.data.get(CONF_ICON, DEFAULT_ICON)
    require_admin: bool = entry.data.get(CONF_REQUIRE_ADMIN, DEFAULT_REQUIRE_ADMIN)

    panel_name = _panel_name(entry)

    try:
        await _register_redirect_resource(hass)
    except Exception as exc:
        LOGGER.error("Could not prepare redirect JS: %s", exc)
        return False

    try:
        async_register_built_in_panel(
            hass,
            component_name="custom",
            sidebar_title=tab_title,
            sidebar_icon=icon,
            frontend_url_path=panel_name,
            config={
                "_panel_custom": {
                    "name": "ha-sidebar-manager-redirect",
                    "embed_iframe": False,
                    "trust_external": False,
                    "module_url": REDIRECT_JS_URL,
                },
                "target": url,
            },
            require_admin=require_admin,
        )
    except Exception as exc:
        LOGGER.error("Failed to register panel %s: %s", tab_title, exc)
        return False

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "panel_name": panel_name,
        "tab_title": tab_title,
        "url": url,
        "icon": icon,
        "require_admin": require_admin,
    }

    entry.async_on_unload(entry.add_update_listener(async_update_listener))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    entry_data = hass.data.get(DOMAIN, {}).pop(entry.entry_id, {})
    panel_name = entry_data.get("panel_name")

    if panel_name:
        try:
            async_remove_panel(hass, panel_name)
        except Exception as exc:
            LOGGER.warning("Could not remove panel %s: %s", panel_name, exc)

    return True


async def async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the config entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)
