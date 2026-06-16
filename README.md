# Concerto

**The open, software-defined universal-remote *activity* engine for Home Assistant.**

Logitech killed Harmony. The replacements are either €279 closed hardware
(Unfolded Circle) or fragmented DIY (scripts, SmartIR, HAIR). **Concerto is the
open, HA-native successor** — it conducts your IR, Bluetooth, and network devices
into *activities* ("Watch TV", "Movie Night", "Power Off"), entirely in software,
on commodity hardware.

> ⚠️ **Status: early / scaffold.** The integration installs and exposes a `remote`
> entity with the activity API; the driver engine and config-flow device/activity
> management are under active construction. Not yet production-ready.

> **Concerto™ is a trademark of HomeOps.** The code is Apache-2.0; the name is not
> — see [TRADEMARK.md](TRADEMARK.md). You may fork the code, but a *modified* fork
> must be renamed.

## Why it exists

An *activity* is one trigger that brings many independent devices into a single
coordinated performance — TV on, soundbar to optical, cable box on, lights dimmed.
That's literally a concerto: a soloist (the activity) set against an orchestra
(the devices), **conducted**. Concerto is that conductor.

It owns the two hard, hardware-flavored capabilities nobody open-sourced as
software, and treats everything else as commodity:

| Layer | What | Where it comes from |
|-------|------|---------------------|
| **Activities** | `remote` entity with `current_activity` / `activity_list` | **Concerto** (this repo) |
| **Capabilities** | power · input · volume · transport · navigate · text | the abstraction Concerto orchestrates |
| **Drivers** | IR · BLE · native · (CEC/RS232) | pluggable — interchangeable transports |
| **IR codes** | raw timings, transmitter-agnostic | [`esphome-ir-codegen`](https://github.com/HomeOps/esphome-ir-codegen) |
| **Bluetooth** | HID over BLE (what UC can't expose to HA) | [`esphome-blekeyboard`](https://github.com/HomeOps/esphome-blekeyboard) |
| **Transmitters / remotes** | ESP proxy, printed remote — *commodity* | `esphome-remote`, any `infrared` entity |

**Input-agnostic** (dashboard, a printed ESP remote, voice, even an Unfolded
Circle button) and **driver-pluggable** (an activity doesn't know whether
`power_on` is an IR blast, a BLE HID press, or a network call). It rides Home
Assistant's 2026.4 `infrared` platform, works with HA-native devices, and can even
drive a UC dock as *one driver* — while depending on none of them.

## Architecture

```
INPUTS (any)              CONCERTO (this repo)          DRIVERS (any)
remote button ─┐                                       ┌─ IR proxy (codes ← codegen)
dashboard ─────┼─▶ remote.turn_on(activity="Watch TV")─┼─ ble_keyboard (BT)
ESP remote ────┤   diff current→target, conduct caps   ├─ HA-native (IP/CEC)
voice ─────────┘                                       └─ UC dock (infrared entity)
```

## Install (HACS)

1. HACS → ⋮ → **Custom repositories** → add `https://github.com/HomeOps/concerto`,
   category **Integration**.
2. Install **Concerto**, restart Home Assistant.
3. **Settings → Devices & Services → Add Integration → Concerto.**

You get a `remote.*` entity. Activities and device drivers are configured from the
integration's UI (config flow / subentries) — no YAML.

## The HomeOps Concerto stack

Concerto conducts; the instruments are separate, reusable repos:

- **[`esphome-ir-codegen`](https://github.com/HomeOps/esphome-ir-codegen)** — the IR code catalog (Flipper-IRDB → raw timings).
- **[`esphome-blekeyboard`](https://github.com/HomeOps/esphome-blekeyboard)** — the BLE HID driver.
- **`esphome-remote`** *(planned)* — a printed, rechargeable, docked ESP input remote.

## License & trademark

Code: [Apache License 2.0](LICENSE). Name: **Concerto™**, a HomeOps trademark —
[TRADEMARK.md](TRADEMARK.md).
