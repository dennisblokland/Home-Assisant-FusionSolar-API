"""
Custom integration to integrate FusionSolar Kiosk with Home Assistant.
"""
import logging

from homeassistant.core import Config, HomeAssistant
from homeassistant.components.sensor import STATE_CLASS_TOTAL_INCREASING, SensorEntity
from homeassistant.const import (
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    ENERGY_KILO_WATT_HOUR,
    POWER_WATT,
    ELECTRIC_POTENTIAL_VOLT,
    ELECTRIC_CURRENT_AMPERE,
    DEVICE_CLASS_TEMPERATURE,
    TEMP_CELSIUS,
    PERCENTAGE
)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import (
    ATTR_DATA_REALKPI,
    DOMAIN,
)


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up the FusionSolar Kiosk component."""
    return True

class FusionSolarKioskBaseEntity(CoordinatorEntity, Entity):
    def __init__(
        self,
        coordinator,
        username,
        password,
        kioskName,
        idSuffix,
        nameSuffix,
        attribute,
    ):

        super().__init__(coordinator)
        self._username = username
        self._password = password
        self._kioskName = kioskName
        self._idSuffix = idSuffix
        self._nameSuffix = nameSuffix
        self._attribute = attribute

    @property
    def name(self):
        return f'{self._kioskName} ({self._username}) - {self._nameSuffix}'

    @property
    def unique_id(self) -> str:
        return f'{DOMAIN}-{self._username}-{self._idSuffix}'

class FusionSolarKioskEnergyEntity(FusionSolarKioskBaseEntity):
    def __init__(
    self,
    coordinator,
    username,
    password,
    kioskName,
    idSuffix,
    nameSuffix,
    attribute,
    ):

        super().__init__(self,coordinator,username, password, kioskName, idSuffix, nameSuffix, attribute)

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_ENERGY

    @property
    def state(self) -> float:
        return float(self.coordinator.data[self._username][ATTR_DATA_REALKPI][self._attribute]) if self.coordinator.data[self._username][ATTR_DATA_REALKPI] else None

    @property
    def unit_of_measurement(self) -> str:
        return ENERGY_KILO_WATT_HOUR

    @property
    def state_class(self) -> str:
        return STATE_CLASS_TOTAL_INCREASING

    @property
    def native_value(self) -> str:
        return self.state if self.state else ''

    @property
    def native_unit_of_measurement(self) -> str:
        return self.unit_of_measurement


class FusionSolarKioskPowerEntity(FusionSolarKioskBaseEntity):
    def __init__(
    self,
    coordinator,
    username,
    password,
    kioskName,
    idSuffix,
    nameSuffix,
    attribute,
    ):

        super().__init__(self,coordinator,username, password, kioskName, idSuffix, nameSuffix, attribute)
    @property
    def device_class(self):
        return DEVICE_CLASS_POWER

    @property
    def state(self):
        return self.coordinator.data[self._username][ATTR_DATA_REALKPI][self._attribute] if self.coordinator.data[self._username][ATTR_DATA_REALKPI] else None

    @property
    def unit_of_measurement(self):
        return POWER_WATT

class FusionSolarKioskVoltageEntity(FusionSolarKioskBaseEntity):
    def __init__(
    self,
    coordinator,
    username,
    password,
    kioskName,
    idSuffix,
    nameSuffix,
    attribute,
    ):

        super().__init__(self,coordinator,username, password, kioskName, idSuffix, nameSuffix, attribute)
    @property
    def device_class(self):
        return DEVICE_CLASS_VOLTAGE

    @property
    def state(self):
        return float(self.coordinator.data[self._username][ATTR_DATA_REALKPI][self._attribute]) if self.coordinator.data[self._username][ATTR_DATA_REALKPI] else None

    @property
    def unit_of_measurement(self):
        return ELECTRIC_POTENTIAL_VOLT

class FusionSolarKioskCurrentEntity(FusionSolarKioskBaseEntity):
    def __init__(
    self,
    coordinator,
    username,
    password,
    kioskName,
    idSuffix,
    nameSuffix,
    attribute,
    ):

        super().__init__(self,coordinator,username, password, kioskName, idSuffix, nameSuffix, attribute)
    @property
    def device_class(self):
        return DEVICE_CLASS_CURRENT

    @property
    def state(self):
        return float(self.coordinator.data[self._username][ATTR_DATA_REALKPI][self._attribute]) if self.coordinator.data[self._username][ATTR_DATA_REALKPI] else None

    @property
    def unit_of_measurement(self):
        return ELECTRIC_CURRENT_AMPERE
class FusionSolarKioskTempratureEntity(FusionSolarKioskBaseEntity):
    def __init__(
    self,
    coordinator,
    username,
    password,
    kioskName,
    idSuffix,
    nameSuffix,
    attribute,
    ):

        super().__init__(self,coordinator,username, password, kioskName, idSuffix, nameSuffix, attribute)

    @property
    def device_class(self):
        return DEVICE_CLASS_TEMPERATURE

    @property
    def state(self):
        return float(self.coordinator.data[self._username][ATTR_DATA_REALKPI][self._attribute]) if self.coordinator.data[self._username][ATTR_DATA_REALKPI] else None

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS
class FusionSolarKioskEfficiencyEntity(FusionSolarKioskBaseEntity):
    def __init__(
    self,
    coordinator,
    username,
    password,
    kioskName,
    idSuffix,
    nameSuffix,
    attribute,
    ):

        super().__init__(self,coordinator,username, password, kioskName, idSuffix, nameSuffix, attribute)

    @property
    def state(self):
        return float(self.coordinator.data[self._username][ATTR_DATA_REALKPI][self._attribute]) if self.coordinator.data[self._username][ATTR_DATA_REALKPI] else None

    @property
    def unit_of_measurement(self):
        return PERCENTAGE

