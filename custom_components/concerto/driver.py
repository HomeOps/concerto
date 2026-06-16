"""Driver interface — the transport layer.

A driver realizes device *capabilities* on a concrete transport (IR via an
`infrared` entity / ESP proxy, BLE via `ble_keyboard`, a native HA service, CEC,
RS232…). Activities call capabilities; drivers decide *how*. New transports plug
in here without the activity engine ever changing.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Driver(ABC):
    """Base class for a device transport driver."""

    @property
    @abstractmethod
    def capabilities(self) -> set[str]:
        """Capabilities this driver can realize.

        e.g. {"power_on", "power_off", "set_input", "volume_up", "volume_down",
        "mute", "navigate", "text"}.
        """

    @abstractmethod
    async def async_realize(self, capability: str, value: str | None = None) -> None:
        """Realize a single capability on the bound device.

        Raises NotImplementedError if the capability is not supported by this
        driver (callers should check `capabilities` first).
        """


# Driver registry. Concrete drivers (ir, ble, native, …) register here so the
# config flow can offer them and the engine can instantiate them by name.
DRIVERS: dict[str, type[Driver]] = {}


def register_driver(name: str):
    """Decorator to register a driver implementation under a stable name."""

    def _wrap(cls: type[Driver]) -> type[Driver]:
        DRIVERS[name] = cls
        return cls

    return _wrap
