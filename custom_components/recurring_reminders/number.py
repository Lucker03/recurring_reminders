"""Number platform for Recurring Reminders integration."""
import logging
from datetime import datetime
from homeassistant.components.number import NumberEntity, NumberMode
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
    """Set up the number platform."""
    
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    config = entry_data["config"]
    
    # Create both number entities for this reminder
    numbers = [
        ReminderIntervalNumber(config_entry, config, entry_data),
        ReminderCountdownNumber(config_entry, config, entry_data)
    ]
    
    async_add_entities(numbers, True)

class ReminderIntervalNumber(NumberEntity):
    """Number entity for the interval in days (editable)."""
    
    def __init__(self, config_entry: ConfigEntry, config: dict, entry_data: dict) -> None:
        """Initialize the number entity."""
        self._config_entry = config_entry
        self._config = config
        self._entry_data = entry_data
        self._attr_name = f"{config['name']} Intervall"
        self._attr_unique_id = f"{config_entry.entry_id}_interval"
        self._attr_native_unit_of_measurement = "Tage"
        self._attr_icon = "mdi:calendar-clock"
        self._attr_mode = NumberMode.BOX
        self._attr_native_min_value = 1
        self._attr_native_max_value = 365
        self._attr_native_step = 1

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.entry_id)},
            name=f"Erinnerung: {self._config['name']}",
            manufacturer="Recurring Reminders",
            model="Reminder",
            sw_version="1.1.0",
        )

    @property
    def native_value(self) -> int:
        """Return the current interval value."""
        # Get the current value from the config entry to ensure it's up to date
        return self._config_entry.data.get("interval", self._config["interval"])

    async def async_set_native_value(self, value: float) -> None:
        """Update the interval value."""
        new_interval = int(value)
        old_interval = self._config["interval"]
        
        try:
            # Update the config entry in Home Assistant (this updates the source)
            self.hass.config_entries.async_update_entry(
                self._config_entry,
                data={**self._config_entry.data, "interval": new_interval}
            )
            
            # Update our local config reference
            self._entry_data["config"] = {**self._config, "interval": new_interval}
            self._config = self._entry_data["config"]
            
            _LOGGER.info(f"Updated interval for '{self._config['name']}' from {old_interval} to {new_interval}")
            
            # Update the state
            self.async_write_ha_state()
            
        except Exception as e:
            _LOGGER.error(f"Error updating interval: {e}")
            raise

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra state attributes."""
        return {
            "reminder_name": self._config["name"],
            "interval_days": self._config["interval"]
        }

class ReminderCountdownNumber(NumberEntity):
    """Number entity for days remaining until next reminder (editable)."""
    
    def __init__(self, config_entry: ConfigEntry, config: dict, entry_data: dict) -> None:
        """Initialize the number entity."""
        self._config_entry = config_entry
        self._config = config
        self._entry_data = entry_data
        self._attr_name = f"{config['name']} Countdown"
        self._attr_unique_id = f"{config_entry.entry_id}_countdown"
        self._attr_native_unit_of_measurement = "Tage"
        self._attr_icon = "mdi:timer-sand"
        self._attr_mode = NumberMode.BOX
        self._attr_native_min_value = 0
        self._attr_native_max_value = 365
        self._attr_native_step = 1

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.entry_id)},
            name=f"Erinnerung: {self._config['name']}",
            manufacturer="Recurring Reminders",
            model="Reminder",
            sw_version="1.1.0",
        )

    @property
    def native_value(self) -> int:
        """Return the current countdown value."""
        return self._entry_data["data"]["days_remaining"]

    async def async_set_native_value(self, value: float) -> None:
        """Update the countdown value."""
        new_days = int(value)
        
        # Update data
        self._entry_data["data"]["days_remaining"] = new_days
        self._entry_data["data"]["last_updated"] = datetime.now().isoformat()
        
        # Save to storage
        await self._entry_data["store"].async_save(self._entry_data["data"])
        
        _LOGGER.info(f"Manually set countdown for '{self._config['name']}' to {new_days} days")
        
        # Update the state
        self.async_write_ha_state()

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
        """Update the countdown state."""
        # Check if we need to update based on time passed
        try:
            last_updated = datetime.fromisoformat(self._entry_data["data"]["last_updated"])
            now = datetime.now()
            days_passed = (now.date() - last_updated.date()).days
            
            if days_passed > 0:
                current_days = self._entry_data["data"]["days_remaining"]
                new_days = max(0, current_days - days_passed)
                
                if new_days != current_days:
                    self._entry_data["data"]["days_remaining"] = new_days
                    self._entry_data["data"]["last_updated"] = now.isoformat()
                    await self._entry_data["store"].async_save(self._entry_data["data"])
                    _LOGGER.info(f"Auto-updated countdown for '{self._config['name']}' to {new_days} days")
                
        except Exception as e:
            _LOGGER.error(f"Error updating countdown: {e}")