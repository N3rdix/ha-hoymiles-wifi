"""Entity base for Hoymiles entities."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_SENSOR_PREFIX, DOMAIN
from .coordinator import HoymilesDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class HoymilesEntity(Entity):
    """Base class for Hoymiles entities."""

    _attr_has_entity_name = True

    def __init__(self, config_entry: ConfigEntry, description: EntityDescription):
        """Initialize the Hoymiles entity."""
        super().__init__()
        self.entity_description = description
        self._config_entry = config_entry
        self._sensor_prefix = f' {config_entry.data.get(CONF_SENSOR_PREFIX)} ' if config_entry.data.get(CONF_SENSOR_PREFIX) else ""
        self._attr_unique_id = f"hoymiles_{config_entry.entry_id}_{description.key}"

        self._dtu_sn = ""
        device_name = "Hoymiles HMS-XXXXW-T2"
        device_model="HMS-XXXXW-T2"


        if hasattr(self.entity_description, "is_dtu_sensor") and self.entity_description.is_dtu_sensor is True:
            device_name += " DTU" + self._sensor_prefix
            device_model += " DTU"
        else:
            device_name += " Inverter"

        device_name += self._sensor_prefix

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.entry_id + device_name)},
            name = device_name,
            manufacturer="Hoymiles",
            serial_number= self._dtu_sn,
            model = device_model
        )


class HoymilesCoordinatorEntity(CoordinatorEntity, HoymilesEntity):
    """Represents a Hoymiles coordinator entity."""

    def __init__(self, config_entry: ConfigEntry, description: EntityDescription, coordinator: HoymilesDataUpdateCoordinator):
        """Pass coordinator to CoordinatorEntity."""
        CoordinatorEntity.__init__(self, coordinator)
        if self.coordinator is not None and hasattr(self.coordinator, "data"):
            self._dtu_sn = getattr(self.coordinator.data, "device_serial_number", "")
        HoymilesEntity.__init__(self, config_entry, description)



