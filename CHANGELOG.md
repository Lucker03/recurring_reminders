# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2025-09-24

### Added
- **NEW**: Configurable friendly names for entities during setup
- **NEW**: Configurable custom icons for countdown entities during setup
- **NEW**: Predictable entity IDs in format `number.recurring_reminders_{{name}}_countdown`

### Changed
- **IMPROVED**: Entity IDs now follow consistent naming pattern
- **IMPROVED**: Dynamic icon behavior based on countdown state (normal/outline/alert variants)
- **IMPROVED**: Friendly names can be different from internal entity names

### Enhanced
- Setup dialog now asks for optional friendly name and icon
- Icons automatically change variants based on countdown state
- Better device naming using friendly names

## [2.1.0] - 2025-09-24

### Changed
- **IMPROVED**: Countdown now updates precisely at midnight (00:00) every day
- **IMPROVED**: More reliable daily countdown updates using `async_track_time_change`
- **IMPROVED**: Better logging for midnight countdown updates

### Fixed
- Fixed unreliable 24-hour interval updates that started from Home Assistant boot time
- Countdown now consistently decrements at midnight regardless of HA restart times

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