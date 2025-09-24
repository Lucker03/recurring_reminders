# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-09-24

### Added
- New service `set_reminder_interval` to change the interval of existing reminders
- Support for using both countdown and interval sensors in all services

### Changed
- Services `reset_reminder` and `set_reminder_days` now accept both countdown and interval sensor entity IDs
- Improved error messages with clearer guidance on which sensor to use
- Better validation of entity IDs in all services

### Fixed
- Services now work with both `_countdown` and `_intervall` sensors for better usability

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