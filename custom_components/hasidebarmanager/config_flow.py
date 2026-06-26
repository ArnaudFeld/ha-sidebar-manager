from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    CONF_ICON,
    CONF_REQUIRE_ADMIN,
    CONF_TAB_TITLE,
    CONF_TEMPLATE_GROUP,
    CONF_TEMPLATE_ITEM,
    CONF_URL,
    DEFAULT_ICON,
    DEFAULT_REQUIRE_ADMIN,
    DEVTOOLS_TEMPLATES,
    DOMAIN,
    TEMPLATE_GROUP_CUSTOM,
    TEMPLATE_GROUP_DEVTOOLS,
)

GROUP_OPTIONS = {
    TEMPLATE_GROUP_DEVTOOLS: "Entwicklerwerkzeuge",
    TEMPLATE_GROUP_CUSTOM: "Benutzerdefiniert",
}

DEVTOOLS_OPTIONS = {
    "state": "Zustände",
    "service": "Dienste",
    "template": "Template",
    "event": "Ereignisse",
    "yaml": "YAML",
    "statistics": "Statistiken",
}


def _group_selector() -> selector.SelectSelector:
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=[
                selector.SelectOptionDict(value=key, label=label)
                for key, label in GROUP_OPTIONS.items()
            ],
            mode=selector.SelectSelectorMode.LIST,
        )
    )


def _devtools_selector() -> selector.SelectSelector:
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=[
                selector.SelectOptionDict(value=key, label=label)
                for key, label in DEVTOOLS_OPTIONS.items()
            ],
            mode=selector.SelectSelectorMode.LIST,
        )
    )


def _custom_schema(defaults: dict | None = None) -> vol.Schema:
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_TAB_TITLE,
                default=defaults.get(CONF_TAB_TITLE, ""),
            ): selector.TextSelector(),
            vol.Required(
                CONF_URL,
                default=defaults.get(CONF_URL, ""),
            ): selector.TextSelector(),
            vol.Optional(
                CONF_ICON,
                default=defaults.get(CONF_ICON, DEFAULT_ICON),
            ): selector.IconSelector(),
            vol.Optional(
                CONF_REQUIRE_ADMIN,
                default=defaults.get(CONF_REQUIRE_ADMIN, DEFAULT_REQUIRE_ADMIN),
            ): selector.BooleanSelector(),
        }
    )


def _devtools_schema(defaults: dict | None = None) -> vol.Schema:
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_TEMPLATE_ITEM,
                default=defaults.get(CONF_TEMPLATE_ITEM, "state"),
            ): _devtools_selector(),
            vol.Optional(
                CONF_TAB_TITLE,
                default=defaults.get(CONF_TAB_TITLE, ""),
            ): selector.TextSelector(),
            vol.Optional(
                CONF_ICON,
                default=defaults.get(CONF_ICON, DEVTOOLS_TEMPLATES["state"]["icon"]),
            ): selector.IconSelector(),
            vol.Optional(
                CONF_REQUIRE_ADMIN,
                default=defaults.get(CONF_REQUIRE_ADMIN, DEFAULT_REQUIRE_ADMIN),
            ): selector.BooleanSelector(),
        }
    )


class HASidebarManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            group = user_input[CONF_TEMPLATE_GROUP]
            if group == TEMPLATE_GROUP_DEVTOOLS:
                return await self.async_step_developer_tools()
            return await self.async_step_custom()

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_TEMPLATE_GROUP,
                    default=TEMPLATE_GROUP_DEVTOOLS,
                ): _group_selector()
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_developer_tools(self, user_input=None):
        if user_input is not None:
            key = user_input[CONF_TEMPLATE_ITEM]
            template = DEVTOOLS_TEMPLATES[key]
            title = user_input.get(CONF_TAB_TITLE, "").strip() or DEVTOOLS_OPTIONS[key]
            icon = user_input.get(CONF_ICON, template["icon"])
            require_admin = user_input.get(
                CONF_REQUIRE_ADMIN,
                template["require_admin"],
            )

            unique = f"{DOMAIN}_{key}_{template['url']}"
            await self.async_set_unique_id(unique)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=title,
                data={
                    CONF_TAB_TITLE: title,
                    CONF_URL: template["url"],
                    CONF_ICON: icon,
                    CONF_REQUIRE_ADMIN: require_admin,
                    CONF_TEMPLATE_GROUP: TEMPLATE_GROUP_DEVTOOLS,
                    CONF_TEMPLATE_ITEM: key,
                },
            )

        defaults = {
            CONF_TEMPLATE_ITEM: "state",
            CONF_TAB_TITLE: "",
            CONF_ICON: DEVTOOLS_TEMPLATES["state"]["icon"],
            CONF_REQUIRE_ADMIN: DEVTOOLS_TEMPLATES["state"]["require_admin"],
        }
        return self.async_show_form(
            step_id="developer_tools",
            data_schema=_devtools_schema(defaults),
        )

    async def async_step_custom(self, user_input=None):
        if user_input is not None:
            unique = f"{DOMAIN}_{user_input[CONF_TAB_TITLE]}_{user_input[CONF_URL]}"
            await self.async_set_unique_id(unique)
            self._abort_if_unique_id_configured()
            user_input[CONF_TEMPLATE_GROUP] = TEMPLATE_GROUP_CUSTOM
            return self.async_create_entry(title=user_input[CONF_TAB_TITLE], data=user_input)

        return self.async_show_form(step_id="custom", data_schema=_custom_schema())

    @staticmethod
    def async_get_options_flow(config_entry):
        return HASidebarManagerOptionsFlow(config_entry)


class HASidebarManagerOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        current_group = self._config_entry.data.get(
            CONF_TEMPLATE_GROUP,
            TEMPLATE_GROUP_DEVTOOLS,
        )

        if user_input is not None:
            group = user_input[CONF_TEMPLATE_GROUP]
            if group == TEMPLATE_GROUP_DEVTOOLS:
                return await self.async_step_edit_devtools()
            return await self.async_step_edit_custom()

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_TEMPLATE_GROUP,
                    default=current_group,
                ): _group_selector()
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)

    async def async_step_edit_devtools(self, user_input=None):
        current_item = self._config_entry.data.get(CONF_TEMPLATE_ITEM, "state")

        if user_input is not None:
            key = user_input[CONF_TEMPLATE_ITEM]
            template = DEVTOOLS_TEMPLATES[key]
            title = user_input.get(CONF_TAB_TITLE, "").strip() or DEVTOOLS_OPTIONS[key]
            icon = user_input.get(CONF_ICON, template["icon"])
            require_admin = user_input.get(
                CONF_REQUIRE_ADMIN,
                template["require_admin"],
            )

            new_data = {
                **self._config_entry.data,
                CONF_TAB_TITLE: title,
                CONF_URL: template["url"],
                CONF_ICON: icon,
                CONF_REQUIRE_ADMIN: require_admin,
                CONF_TEMPLATE_GROUP: TEMPLATE_GROUP_DEVTOOLS,
                CONF_TEMPLATE_ITEM: key,
            }

            self.hass.config_entries.async_update_entry(
                self._config_entry,
                title=title,
                data=new_data,
            )
            return self.async_create_entry(title="", data={})

        template = DEVTOOLS_TEMPLATES[current_item]
        defaults = {
            CONF_TEMPLATE_ITEM: current_item,
            CONF_TAB_TITLE: self._config_entry.data.get(CONF_TAB_TITLE, ""),
            CONF_ICON: self._config_entry.data.get(CONF_ICON, template["icon"]),
            CONF_REQUIRE_ADMIN: self._config_entry.data.get(
                CONF_REQUIRE_ADMIN,
                template["require_admin"],
            ),
        }
        return self.async_show_form(
            step_id="edit_devtools",
            data_schema=_devtools_schema(defaults),
        )

    async def async_step_edit_custom(self, user_input=None):
        if user_input is not None:
            new_data = {
                **self._config_entry.data,
                CONF_TAB_TITLE: user_input[CONF_TAB_TITLE],
                CONF_URL: user_input[CONF_URL],
                CONF_ICON: user_input.get(CONF_ICON, DEFAULT_ICON),
                CONF_REQUIRE_ADMIN: user_input.get(CONF_REQUIRE_ADMIN, DEFAULT_REQUIRE_ADMIN),
                CONF_TEMPLATE_GROUP: TEMPLATE_GROUP_CUSTOM,
            }
            new_data.pop(CONF_TEMPLATE_ITEM, None)

            self.hass.config_entries.async_update_entry(
                self._config_entry,
                title=user_input[CONF_TAB_TITLE],
                data=new_data,
            )
            return self.async_create_entry(title="", data={})

        current = {
            CONF_TAB_TITLE: self._config_entry.data.get(CONF_TAB_TITLE, ""),
            CONF_URL: self._config_entry.data.get(CONF_URL, ""),
            CONF_ICON: self._config_entry.data.get(CONF_ICON, DEFAULT_ICON),
            CONF_REQUIRE_ADMIN: self._config_entry.data.get(CONF_REQUIRE_ADMIN, DEFAULT_REQUIRE_ADMIN),
        }
        return self.async_show_form(step_id="edit_custom", data_schema=_custom_schema(current))
