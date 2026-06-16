"""Tests for the Concerto remote entity."""

from homeassistant.components.remote import RemoteEntityFeature
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.concerto.const import DOMAIN


async def test_remote_entity_created(hass: HomeAssistant) -> None:
    """Setting up an entry creates a remote with the activity feature."""
    entry = MockConfigEntry(
        domain=DOMAIN, title="Living Room", data={"name": "Living Room"}
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get("remote.living_room")
    assert state is not None
    assert state.state == "off"

    features = state.attributes["supported_features"]
    assert features & RemoteEntityFeature.ACTIVITY
