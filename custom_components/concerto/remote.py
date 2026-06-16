"""The Concerto `remote` entity — the activity API surface.

Exposes Home Assistant's native activity model (`activity_list`,
`current_activity`, `remote.turn_on(activity=...)`). Conducting the drivers to
realize a transition is wired in as devices/activities are added (config
subentries); for now this is the entity scaffold with the correct API shape.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from homeassistant.components.remote import RemoteEntity, RemoteEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Concerto remote from a config entry."""
    async_add_entities([ConcertoRemote(entry)])


class ConcertoRemote(RemoteEntity):
    """A universal remote whose activities conduct multiple devices."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_supported_features = RemoteEntityFeature.ACTIVITY

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the Concerto remote."""
        self._entry = entry
        self._attr_unique_id = entry.entry_id
        self._attr_is_on = False
        self._attr_current_activity = None
        self._attr_activity_list: list[str] = []  # populated from subentries

    @property
    def device_info(self) -> DeviceInfo:
        """Group the entity under a Concerto device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self._entry.title,
            manufacturer="HomeOps",
            model="Concerto",
        )

    async def async_turn_on(self, activity: str | None = None, **kwargs: Any) -> None:
        """Start an activity — conduct the transition to its desired state.

        TODO: diff current_activity -> target, power off devices no longer
        needed, power on new ones, set inputs, via each device's driver.
        """
        self._attr_current_activity = activity
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Stop the current activity — power off its devices."""
        self._attr_current_activity = None
        self._attr_is_on = False
        self.async_write_ha_state()

    async def async_send_command(self, command: Iterable[str], **kwargs: Any) -> None:
        """Send an ad-hoc command to a bound device's driver.

        TODO: route `command` to the target device's driver capability.
        """
