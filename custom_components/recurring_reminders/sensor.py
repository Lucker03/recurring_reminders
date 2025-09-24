"""Sensor platform for Recurring Reminders integration."""
import logging
from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    config = entry_data["config"]
    
    # Create both sensors for this reminder
    sensors = [
        ReminderIntervalSensor(config_entry, config),
        ReminderCountdownSensor(config_entry, config, entry_data)
    ]
    
    async_add_entities(sensors, True)

class ReminderIntervalSensor(SensorEntity):
    """Sensor showing the interval in days."""
    
    def __init__(self, config_entry: ConfigEntry, config: dict) -> None:
        """Initialize the sensor."""
        self._config_entry = config_entry
        self._config = config
        self._attr_name = f"{config['name']} Intervall"
        self._attr_unique_id = f"{config_entry.entry_id}_interval"
        self._attr_native_unit_of_measurement = "Tage"
        self._attr_icon = "mdi:calendar-clock"
        self._attr_state_class = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.entry_id)},
            name=f"Erinnerung: {self._config['name']}",
            manufacturer="Recurring Reminders",
            model="Reminder",
            sw_version="1.0.0",
        )

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        return self._config["interval"]

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra state attributes."""
        return {
            "reminder_name": self._config["name"],
            "interval_days": self._config["interval"]
        }

class ReminderCountdownSensor(SensorEntity):
    """Sensor showing days remaining until next reminder."""
    
    def __init__(self, config_entry: ConfigEntry, config: dict, entry_data: dict) -> None:
        """Initialize the sensor."""
        self._config_entry = config_entry
        self._config = config
        self._entry_data = entry_data
        self._attr_name = f"{config['name']} Countdown"
        self._attr_unique_id = f"{config_entry.entry_id}_countdown"
        self._attr_native_unit_of_measurement = "Tage"
        self._attr_icon = "mdi:timer-sand"
        self._attr_state_class = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.entry_id)},
            name=f"Erinnerung: {self._config['name']}",
            manufacturer="Recurring Reminders",
            model="Reminder",
            sw_version="1.0.0",
        )

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        return self._entry_data["data"]["days_remaining"]

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra state attributes."""
        return {
            "reminder_name": self._config["name"],
            "interval_days": self._config["interval"],
            "last_updated": self._entry_data["data"]["last_updated"],
            "is_due": self._entry_data["data"]["days_remaining"] == 0
        }

    @property
    def icon(self) -> str:
        """Return the icon based on state."""
        if self._entry_data["data"]["days_remaining"] == 0:
            return "mdi:bell-ring"
        elif self._entry_data["data"]["days_remaining"] <= 1:
            return "mdi:timer-sand-empty"
        else:
            return "mdi:timer-sand"

    async def async_update(self) -> None:
        """Update the sensor state."""
        # Check if we need to update based on time passed
        try:
            last_updated = datetime.fromisoformat(self._entry_data["data"]["last_updated"])
            now = datetime.now()
            days_passed = (now.date() - last_updated.date()).days
            
            if days_passed > 0:
                current_days = self._entry_data["data"]["days_remaining"]
                new_days = max(0, current_days - days_passed)
                
                self._entry_data["data"]["days_remaining"] = new_days
                self._entry_data["data"]["last_updated"] = now.isoformat()
                await self._entry_data["store"].async_save(self._entry_data["data"])
                
        except Exception as e:
            _LOGGER.error(f"Error updating countdown sensor: {e}")