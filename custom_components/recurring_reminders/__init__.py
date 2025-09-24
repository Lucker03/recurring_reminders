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
PLATFORMS = [Platform.SENSOR]
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
    
    # Register services
    async def reset_reminder(call: ServiceCall) -> None:
        """Reset the reminder countdown."""
        entity_id = call.data.get("entity_id")
        if not entity_id:
            _LOGGER.error("No entity_id provided for reset_reminder service")
            return
        
        # Support both countdown and interval sensors
        is_countdown = "_countdown" in entity_id
        is_interval = "_intervall" in entity_id
        
        if not is_countdown and not is_interval:
            _LOGGER.error(f"Invalid entity_id: {entity_id}. Please use either countdown sensor (ending with '_countdown') or interval sensor (ending with '_intervall')")
            return
            
        # Extract entry_id from entity_id
        try:
            if is_countdown:
                name_part = entity_id.replace("sensor.recurring_reminders_", "").replace("_countdown", "")
                countdown_entity = entity_id
            else:  # is_interval
                name_part = entity_id.replace("sensor.recurring_reminders_", "").replace("_intervall", "")
                countdown_entity = f"sensor.recurring_reminders_{name_part}_countdown"
            
            target_entry = None
            
            for entry_id, entry_data in hass.data[DOMAIN].items():
                if entry_data["config"]["name"].lower().replace(" ", "_") == name_part:
                    target_entry = entry_id
                    break
            
            if target_entry:
                entry_data = hass.data[DOMAIN][target_entry]
                entry_data["data"]["days_remaining"] = entry_data["config"]["interval"]
                entry_data["data"]["last_updated"] = datetime.now().isoformat()
                await entry_data["store"].async_save(entry_data["data"])
                
                # Update the countdown sensor
                hass.states.async_set(
                    countdown_entity,
                    entry_data["data"]["days_remaining"],
                    {"last_reset": datetime.now().isoformat()}
                )
                _LOGGER.info(f"Reset reminder for {countdown_entity}")
            else:
                _LOGGER.error(f"Could not find reminder for entity {entity_id}")
                
        except Exception as e:
            _LOGGER.error(f"Error resetting reminder: {e}")
    
    async def set_reminder_days(call: ServiceCall) -> None:
        """Set custom days for reminder countdown."""
        entity_id = call.data.get("entity_id")
        days = call.data.get("days")
        
        if not entity_id or days is None:
            _LOGGER.error("entity_id and days are required for set_reminder_days service")
            return
        
        # Support both countdown and interval sensors
        is_countdown = "_countdown" in entity_id
        is_interval = "_intervall" in entity_id
        
        if not is_countdown and not is_interval:
            _LOGGER.error(f"Invalid entity_id: {entity_id}. Please use either countdown sensor (ending with '_countdown') or interval sensor (ending with '_intervall')")
            return
            
        try:
            if is_countdown:
                name_part = entity_id.replace("sensor.recurring_reminders_", "").replace("_countdown", "")
                countdown_entity = entity_id
            else:  # is_interval
                name_part = entity_id.replace("sensor.recurring_reminders_", "").replace("_intervall", "")
                countdown_entity = f"sensor.recurring_reminders_{name_part}_countdown"
            
            target_entry = None
            
            for entry_id, entry_data in hass.data[DOMAIN].items():
                if entry_data["config"]["name"].lower().replace(" ", "_") == name_part:
                    target_entry = entry_id
                    break
            
            if target_entry:
                entry_data = hass.data[DOMAIN][target_entry]
                entry_data["data"]["days_remaining"] = int(days)
                entry_data["data"]["last_updated"] = datetime.now().isoformat()
                await entry_data["store"].async_save(entry_data["data"])
                
                # Update the countdown sensor
                hass.states.async_set(
                    countdown_entity,
                    entry_data["data"]["days_remaining"],
                    {"manually_set": datetime.now().isoformat()}
                )
                _LOGGER.info(f"Set reminder days to {days} for {countdown_entity}")
            else:
                _LOGGER.error(f"Could not find reminder for entity {entity_id}")
                
        except Exception as e:
            _LOGGER.error(f"Error setting reminder days: {e}")
    
    async def set_reminder_interval(call: ServiceCall) -> None:
        """Set new interval for reminder."""
        entity_id = call.data.get("entity_id")
        interval = call.data.get("interval")
        
        if not entity_id or interval is None:
            _LOGGER.error("entity_id and interval are required for set_reminder_interval service")
            return
        
        # Normalize entity_id - handle both full and shortened versions
        if not entity_id.startswith("sensor."):
            entity_id = f"sensor.{entity_id}"
        
        # Check if it's a recurring_reminders sensor
        if not "recurring_reminders" in entity_id:
            # Try to find matching reminder by name
            possible_matches = []
            for entry_id, entry_data in hass.data[DOMAIN].items():
                reminder_name = entry_data["config"]["name"].lower().replace(" ", "_")
                if reminder_name in entity_id.lower():
                    possible_matches.append((entry_id, entry_data, reminder_name))
            
            if len(possible_matches) == 1:
                target_entry, entry_data, reminder_name = possible_matches[0]
                entity_id = f"sensor.recurring_reminders_{reminder_name}_intervall"
            else:
                _LOGGER.error(f"Could not find unique reminder for entity {entity_id}. Available reminders: {[data['config']['name'] for _, data in hass.data[DOMAIN].items()]}")
                return
        
        # Check if user provided countdown sensor instead of interval sensor
        if "_countdown" in entity_id:
            entity_id = entity_id.replace("_countdown", "_intervall")
            _LOGGER.info(f"Switching to interval sensor: {entity_id}")
            
        if not ("_intervall" in entity_id or "_interval" in entity_id):
            # Try to append _intervall if not present
            if entity_id.endswith("_countdown"):
                entity_id = entity_id.replace("_countdown", "_intervall")
            else:
                entity_id = f"{entity_id}_intervall"
            _LOGGER.info(f"Assuming interval sensor: {entity_id}")
            
        try:
            # Extract name part more robustly
            name_part = entity_id.replace("sensor.recurring_reminders_", "").replace("sensor.", "")
            name_part = name_part.replace("_intervall", "").replace("_interval", "")
            
            target_entry = None
            
            for entry_id, entry_data in hass.data[DOMAIN].items():
                reminder_name = entry_data["config"]["name"].lower().replace(" ", "_")
                if reminder_name == name_part or name_part in reminder_name or reminder_name in name_part:
                    target_entry = entry_id
                    break
            
            if target_entry:
                # Update the config entry with new interval
                entry_data = hass.data[DOMAIN][target_entry]
                old_interval = entry_data["config"]["interval"]
                entry_data["config"]["interval"] = int(interval)
                
                # Update the config entry in Home Assistant
                config_entry = hass.config_entries.async_get_entry(target_entry)
                hass.config_entries.async_update_entry(
                    config_entry,
                    data={**config_entry.data, "interval": int(interval)}
                )
                
                # Construct correct entity IDs
                correct_name = entry_data["config"]["name"].lower().replace(" ", "_")
                interval_entity = f"sensor.recurring_reminders_{correct_name}_intervall"
                
                # Update the interval sensor state
                hass.states.async_set(
                    interval_entity,
                    int(interval),
                    {"old_interval": old_interval, "updated": datetime.now().isoformat()}
                )
                
                _LOGGER.info(f"Updated interval for {interval_entity} from {old_interval} to {interval}")
            else:
                _LOGGER.error(f"Could not find reminder for entity {entity_id}. Available reminders: {[data['config']['name'] for _, data in hass.data[DOMAIN].items()]}")
                
        except Exception as e:
            _LOGGER.error(f"Error setting reminder interval: {e}")

    # Register services
    hass.services.async_register(DOMAIN, "reset_reminder", reset_reminder)
    hass.services.async_register(DOMAIN, "set_reminder_days", set_reminder_days)
    hass.services.async_register(DOMAIN, "set_reminder_interval", set_reminder_interval)
    
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