# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-09-24

### Breaking Changes
- **MAJOR**: Replaced sensor entities with number entities for direct editing
- **MAJOR**: Removed all custom services - use native Home Assistant controls instead
- Entity names changed from `sensor.*` to `number.*`

### Added
- Number entities that can be directly edited in Home Assistant UI
- Native Home Assistant controls (sliders, input boxes)
- No more need for custom services or automations to change values

### Changed
- Interval and countdown are now `number` entities instead of `sensor` entities
- Values can be changed directly through Home Assistant interface
- Simplified architecture without custom services

### Removed
- All custom services (`reset_reminder`, `set_reminder_days`, `set_reminder_interval`)
- `services.yaml` file
- Sensor platform (`sensor.py`)

## [1.0.0] - 2025-09-24

### Added
- Initial release
- Configurable recurring reminders with custom intervals
- Interval and countdown sensors for each reminder
- Services to reset reminders and set custom countdown values
- Automatic daily countdown updates
- HACS support
- German localization for config flow

### Features
- Two sensors per reminder (interval and countdown)
- Services: `reset_reminder` and `set_reminder_days`
- Persistent storage of reminder states
- Automatic countdown updates at midnight
- Visual indicators when reminders are due (bell icon)

[1.0.0]: https://github.com/Lucker03/recurring_reminders/releases/tag/v1.0.0