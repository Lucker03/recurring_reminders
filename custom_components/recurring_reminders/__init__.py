"""Recurring Reminders Integration for Home Assistant."""
import logging
from datetime import datetime, timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.storage import Store
from homeassistant.helpers.event import async_track_time_change
from homeassistant.const import Platform

_LOGGER = logging.getLogger(__name__)

DOMAIN = "recurring_reminders"
PLATFORMS = [Platform.NUMBER]
STORAGE_VERSION = 1

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Recurring Reminders component."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Recurring Reminders from a config entry."""
    
    # Initialize storage
    store = Store(hass, STORAGE_VERSION, f"{DOMAIN}_{entry.entry_id}")
    data = await store.async_load() or {}
    
    # Initialize reminder data if not exists
    if "last_updated" not in data:
        data["last_updated"] = datetime.now().isoformat()
        data["days_remaining"] = entry.data["interval"]
        await store.async_save(data)
    
    # Store data in hass.data
    hass.data[DOMAIN][entry.entry_id] = {
        "store": store,
        "data": data,
        "config": entry.data
    }
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    async def midnight_countdown_update(now):
        """Update countdown every midnight."""
        _LOGGER.info("Running midnight countdown update for all reminders")
        
        for entry_id, entry_data in hass.data[DOMAIN].items():
            try:
                current_days = entry_data["data"]["days_remaining"]
                reminder_name = entry_data["config"]["name"]
                
                # Only reduce if not already at 0
                if current_days > 0:
                    new_days = current_days - 1
                    entry_data["data"]["days_remaining"] = new_days
                    entry_data["data"]["last_updated"] = now.isoformat()
                    await entry_data["store"].async_save(entry_data["data"])
                    
                    _LOGGER.info(f"Countdown for '{reminder_name}' updated from {current_days} to {new_days}")
                    
                    # Update number entity state
                    name_normalized = reminder_name.lower().replace(" ", "_").replace("-", "_")
                    countdown_entity_id = f"number.recurring_reminders_{name_normalized}_countdown"
                    hass.states.async_set(countdown_entity_id, new_days)
                else:
                    _LOGGER.debug(f"Countdown for '{reminder_name}' stays at 0 (due)")
                    
            except Exception as e:
                _LOGGER.error(f"Error in midnight update for entry {entry_id}: {e}")
    
    # Schedule daily updates at midnight (00:00)
    from homeassistant.helpers.event import async_track_time_change
    async_track_time_change(hass, midnight_countdown_update, hour=0, minute=0, second=0)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok