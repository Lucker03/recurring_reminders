# Release Description für GitHub

Kopieren Sie diesen Text in die Release-Beschreibung:

---

## 🎉 Initial Release v1.0.0

### ✨ Added
- Initial release
- Configurable recurring reminders with custom intervals
- Interval and countdown sensors for each reminder
- Services to reset reminders and set custom countdown values
- Automatic daily countdown updates
- HACS support
- German localization for config flow

### 🔧 Features
- Two sensors per reminder (interval and countdown)
- Services: `reset_reminder` and `set_reminder_days`
- Persistent storage of reminder states
- Automatic countdown updates at midnight
- Visual indicators when reminders are due (bell icon)

### 📦 Installation via HACS
1. Add this repository as a custom HACS repository
2. Install "Recurring Reminders" 
3. Restart Home Assistant
4. Add integration via Settings → Devices & Services

### 🐛 Support
Please report issues at: https://github.com/Lucker03/recurring_reminders/issues

---