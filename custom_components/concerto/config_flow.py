"""Config flow for Concerto.

UI-driven, no YAML. v1 creates the Concerto hub (a named `remote` entity). Device
and activity management arrive as config subentries — the orchestration the
`remote` entity conducts.
"""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import CONF_NAME, DOMAIN


class ConcertoConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the Concerto config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Create a Concerto hub."""
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_NAME, default="Concerto"): str}),
        )
