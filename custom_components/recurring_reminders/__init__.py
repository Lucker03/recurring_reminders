"""Recurring Reminders Integration for Home Assistant."""
import logging
from datetime import datetime, timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.storage import Store
from homeassistant.helpers.event import async_track_time_interval
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
    
    # Set up daily countdown update
    async def daily_update(now):
        """Update countdown daily."""
        for entry_id, entry_data in hass.data[DOMAIN].items():
            try:
                last_updated = datetime.fromisoformat(entry_data["data"]["last_updated"])
                days_passed = (now.date() - last_updated.date()).days
                
                if days_passed > 0:
                    current_days = entry_data["data"]["days_remaining"]
                    new_days = max(0, current_days - days_passed)
                    
                    entry_data["data"]["days_remaining"] = new_days
                    entry_data["data"]["last_updated"] = now.isoformat()
                    await entry_data["store"].async_save(entry_data["data"])
                    
                    # Update sensor state
                    entity_id = f"sensor.recurring_reminders_{entry_data['config']['name'].lower().replace(' ', '_')}_countdown"
                    hass.states.async_set(entity_id, new_days)
                    
            except Exception as e:
                _LOGGER.error(f"Error in daily update for entry {entry_id}: {e}")
    
    # Schedule daily updates at midnight
    async_track_time_interval(hass, daily_update, timedelta(hours=24))
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok