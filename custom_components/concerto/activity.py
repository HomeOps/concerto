"""Activity model — the logical layer Concerto conducts.

An activity is transport-agnostic: it describes a *desired state* across devices
(power, input, routing). It says nothing about HOW each capability is realized —
that is the driver's job. This separation is the whole point: the same activity
can mix IR, BLE, and network drivers.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ActivityStep:
    """One device's desired state within an activity."""

    device: str  # device id (bound to a driver)
    capability: str  # e.g. "power_on", "set_input"
    value: str | None = None  # e.g. the input name for set_input


@dataclass(slots=True)
class Activity:
    """A coordinated multi-device state — the 'soloist' Concerto foregrounds."""

    name: str
    steps: list[ActivityStep] = field(default_factory=list)
    # Which device handles volume/transport while this activity is active.
    volume_device: str | None = None

    @property
    def devices(self) -> set[str]:
        """Devices this activity powers on."""
        return {step.device for step in self.steps}
