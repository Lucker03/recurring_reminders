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
    
    async def reset_reminder(call: ServiceCall) -> None:
        """Reset a countdown to its interval value."""
        entity_id = call.data.get("entity_id")
        
        if not entity_id:
            _LOGGER.error("No entity_id provided for reset_reminder service")
            return
            
        # Check if it's a countdown entity
        if not entity_id.endswith("_countdown"):
            _LOGGER.error(f"Entity {entity_id} is not a countdown entity")
            return
            
        # Get the entity state to retrieve attributes
        state = hass.states.get(entity_id)
        if not state:
            _LOGGER.error(f"Entity {entity_id} not found")
            return
            
        # Get the interval_days from attributes
        interval_days = state.attributes.get("interval_days")
        if interval_days is None:
            _LOGGER.error(f"No interval_days attribute found for {entity_id}")
            return
            
        try:
            # Find the corresponding entry_data
            entry_data = None
            reminder_name = state.attributes.get("reminder_name")
            
            for entry_id, data in hass.data[DOMAIN].items():
                if data.get("config", {}).get("name") == reminder_name:
                    entry_data = data
                    break
                    
            if not entry_data:
                _LOGGER.error(f"Could not find entry data for {entity_id}")
                return
                
            # Update the countdown value
            entry_data["data"]["days_remaining"] = int(interval_days)
            entry_data["data"]["last_updated"] = datetime.now().isoformat()
            await entry_data["store"].async_save(entry_data["data"])
            
            # Update the entity state
            hass.states.async_set(entity_id, int(interval_days))
            
            _LOGGER.info(f"Reset countdown {entity_id} to {interval_days} days")
            
        except Exception as e:
            _LOGGER.error(f"Error resetting reminder {entity_id}: {e}")
    
    # Register the service
    hass.services.async_register(
        DOMAIN,
        "reset_reminder", 
        reset_reminder,
        schema=None  # We'll validate manually in the function
    )
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        # Clean up stored data
        entry_data = hass.data[DOMAIN].pop(entry.entry_id, None)
        if entry_data and "store" in entry_data:
            # Optionally clean up storage file
            try:
                store = entry_data["store"]
                # Note: We keep the storage file for potential future use
                # To completely remove: await store.async_remove()
                _LOGGER.info(f"Unloaded reminder: {entry_data['config']['name']}")
            except Exception as e:
                _LOGGER.error(f"Error during cleanup: {e}")
    
    return unload_ok

async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Remove a config entry and clean up storage."""
    entry_data = hass.data[DOMAIN].get(entry.entry_id)
    if entry_data and "store" in entry_data:
        try:
            store = entry_data["store"]
            await store.async_remove()
            _LOGGER.info(f"Removed storage for reminder: {entry_data['config']['name']}")
        except Exception as e:
            _LOGGER.error(f"Error removing storage: {e}")