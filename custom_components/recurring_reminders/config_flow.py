"""Config flow for Recurring Reminders integration."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required("name", description="Name der Erinnerung"): str,
    vol.Required("interval", description="Intervall in Tagen"): vol.All(vol.Coerce(int), vol.Range(min=1, max=365))
})

async def validate_input(hass: HomeAssistant, data: dict) -> dict:
    """Validate the user input allows us to connect."""
    
    # Check if name is already used
    for entry in hass.config_entries.async_entries(DOMAIN):
        if entry.data.get("name", "").lower() == data["name"].lower():
            raise ValueError("Name bereits verwendet")
    
    return {"title": f"Erinnerung: {data['name']}"}

class RecurringRemindersConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Recurring Reminders."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                
                return self.async_create_entry(title=info["title"], data=user_input)
            except ValueError as e:
                errors["base"] = str(e)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", 
            data_schema=DATA_SCHEMA, 
            errors=errors,
            description_placeholders={
                "name": "z.B. 'Flur saugen'",
                "interval": "z.B. 7 für wöchentlich"
            }
        )