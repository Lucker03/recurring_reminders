# Recurring Reminders

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

_Integration to manage recurring reminders and tasks in Home Assistant._

**This integration will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show interval and countdown for recurring reminders.

## Features

- **Configurable Reminders**: Create reminders with custom intervals (in days)
- **Two Sensors per Reminder**:
  - **Interval Sensor**: Shows the configured interval in days
  - **Countdown Sensor**: Counts down the days until the next reminder
- **Services for Interaction**:
  - `recurring_reminders.reset_reminder`: Reset the countdown
  - `recurring_reminders.set_reminder_days`: Set countdown to a custom value

## Installation

### HACS (Recommended)

1. In the HACS GUI, go to "Integrations"
2. Click the three dots in the top right corner and select "Custom repositories"
3. Add this repository URL and select "Integration" as the category
4. Click "Install" on the "Recurring Reminders" integration
5. Restart Home Assistant
6. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Recurring Reminders"

### Manual Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`)
2. If you do not have a `custom_components` directory (folder) there, you need to create it
3. In the `custom_components` directory (folder) create a new folder called `recurring_reminders`
4. Download _all_ the files from the `custom_components/recurring_reminders/` directory (folder) in this repository
5. Place the files you downloaded in the new directory (folder) you created
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Recurring Reminders"

## Configuration

When adding a new reminder, you will be asked for:

- **Reminder Name**: e.g., "Vacuum hallway"
- **Interval in Days**: e.g., 7 for weekly

## Usage

### Sensors

For each reminder, two sensors are created:

1. `sensor.recurring_reminders_[name]_interval` - Shows the interval
2. `sensor.recurring_reminders_[name]_countdown` - Shows remaining days

### Services

#### reset_reminder
Resets a reminder's countdown to the original interval.

```yaml
service: recurring_reminders.reset_reminder
data:
  entity_id: sensor.recurring_reminders_vacuum_hallway_countdown
```

#### set_reminder_days
Sets the countdown to a custom value.

```yaml
service: recurring_reminders.set_reminder_days
data:
  entity_id: sensor.recurring_reminders_vacuum_hallway_countdown
  days: 3
```

### Automations

You can create automations based on the sensors:

```yaml
automation:
  - alias: "Reminder: Vacuum hallway"
    trigger:
      - platform: state
        entity_id: sensor.recurring_reminders_vacuum_hallway_countdown
        to: "0"
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "Time to vacuum the hallway!"
          title: "Household Reminder"
```

## Example Dashboard Card

```yaml
type: entities
title: Household Reminders
entities:
  - entity: sensor.recurring_reminders_vacuum_hallway_countdown
    name: Vacuum hallway
    icon: mdi:vacuum
  - entity: sensor.recurring_reminders_clean_bathroom_countdown
    name: Clean bathroom
    icon: mdi:spray-bottle
```

## How it works

- The countdown is automatically reduced by 1 daily
- When it reaches 0, the value stays at 0
- The `reset_reminder` service resets the value back to the original interval
- The `set_reminder_days` service allows manual adjustments for exceptions

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

---

[recurring_reminders]: https://github.com/yourusername/recurring_reminders
[commits-shield]: https://img.shields.io/github/commit-activity/y/yourusername/recurring_reminders.svg?style=for-the-badge
[commits]: https://github.com/yourusername/recurring_reminders/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/yourusername/recurring_reminders.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/yourusername/recurring_reminders.svg?style=for-the-badge
[releases]: https://github.com/yourusername/recurring_reminders/releases