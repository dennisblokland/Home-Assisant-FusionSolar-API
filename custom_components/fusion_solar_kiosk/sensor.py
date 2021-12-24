"""FusionSolar Kiosk sensor."""
from .fusion_solar_kiosk_api import *
import homeassistant.helpers.config_validation as cv
import logging
import voluptuous as vol

from . import FusionSolarKioskEnergyEntity, FusionSolarKioskPowerEntity, FusionSolarKioskVoltageEntity, FusionSolarKioskCurrentEntity, FusionSolarKioskTempratureEntity, FusionSolarKioskEfficiencyEntity

from datetime import timedelta
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_NAME,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import *

KIOSK_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_NAME): cv.string
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_KIOSKS): vol.All(cv.ensure_list, [KIOSK_SCHEMA]),
    }
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async def async_update_data():
        """Fetch data"""
        data = {}
        api = FusionSolarKioksApi()
        for kiosk in config[CONF_KIOSKS]:
            data[kiosk['username']] = {
                ATTR_DATA_REALKPI: await hass.async_add_executor_job(api.getRealTimeKpi, kiosk['username'], kiosk['password'])
            }

        return data


    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name='FusionSolarAPI',
        update_method=async_update_data,
        update_interval=timedelta(seconds=300),
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    async_add_entities(
        FusionSolarKioskSensorRealtimePower(
            coordinator,
            kiosk['username'],
            kiosk['password'],
            kiosk['name'],
            ID_REALTIME_POWER,
            NAME_REALTIME_POWER,
            ATTR_REALTIME_POWER,
        ) for kiosk in config[CONF_KIOSKS]
    )
    async_add_entities(
        FusionSolarKioskSensorTotalCurrentDayEnergy(
            coordinator,
            kiosk['username'],
            kiosk['password'],
            kiosk['name'],
            ID_TOTAL_CURRENT_DAY_ENERGY,
            NAME_TOTAL_CURRENT_DAY_ENERGY,
            ATTR_TOTAL_CURRENT_DAY_ENERGY,
        ) for kiosk in config[CONF_KIOSKS]
    )
    async_add_entities(
        FusionSolarKioskSensorTotalCurrentMonthEnergy(
            coordinator,
            kiosk['username'],
            kiosk['password'],
            kiosk['name'],
            ID_TOTAL_CURRENT_MONTH_ENERGY,
            NAME_TOTAL_CURRENT_MONTH_ENERGY,
            ATTR_TOTAL_CURRENT_MONTH_ENERGY,
        ) for kiosk in config[CONF_KIOSKS]
    )

    async_add_entities(
        FusionSolarKioskSensorTotalLifetimeEnergy(
            coordinator,
            kiosk['username'],
            kiosk['password'],
            kiosk['name'],
            ID_TOTAL_LIFETIME_ENERGY,
            NAME_TOTAL_LIFETIME_ENERGY,
            ATTR_TOTAL_LIFETIME_ENERGY,
        ) for kiosk in config[CONF_KIOSKS]
    )
    async_add_entities(
        FusionSolarKioskTempratureEntity(
            coordinator,
            kiosk['username'],
            kiosk['password'],
            kiosk['name'],
            ID_TEMPRATURE,
            NAME_TEMPRATURE,
            ATTR_TEMPRATURE,
        ) for kiosk in config[CONF_KIOSKS]
    )
    async_add_entities(
        FusionSolarKioskEfficiencyEntity(
            coordinator,
            kiosk['username'],
            kiosk['password'],
            kiosk['name'],
            ID_EFFICIENCY,
            NAME_EFFICIENCY,
            ATTR_EFFICIENCY,
        ) for kiosk in config[CONF_KIOSKS]
    )


    for kiosk in config[CONF_KIOSKS]:
        async_add_entities(
            FusionSolarKioskVoltageEntity(
                coordinator,
                kiosk['username'],
                kiosk['password'],
                kiosk['name'],
                ID_VOLTAGE + str(i),
                NAME_VOLTAGE + " " + str(i),
                ATTR_VOLTAGE + str(i),
            ) for i in range(1,9)
        )

    for kiosk in config[CONF_KIOSKS]:
        async_add_entities(
            FusionSolarKioskCurrentEntity(
                coordinator,
                kiosk['username'],
                kiosk['password'],
                kiosk['name'],
                ID_CURRENT + str(i),
                NAME_CURRENT + " " + str(i),
                ATTR_CURRENT + str(i),
            ) for i in range(1,9)
        )
        


class FusionSolarKioskSensorRealtimePower(FusionSolarKioskPowerEntity):
    pass

class FusionSolarKioskSensorTotalCurrentDayEnergy(FusionSolarKioskEnergyEntity):
    pass

class FusionSolarKioskSensorTotalCurrentMonthEnergy(FusionSolarKioskEnergyEntity):
    pass
class FusionSolarKioskSensorTotalLifetimeEnergy(FusionSolarKioskEnergyEntity):
    pass
