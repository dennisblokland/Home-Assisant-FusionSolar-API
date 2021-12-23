"""API client for FusionSolar Kiosk."""
import logging
import html
import json
from .fusionsolar import Client, PandasClient
import  pandas as pd

from .const import (
    ATTR_DATA,
    ATTR_DATA_ITEMMAP,
    ATTR_FAIL_CODE,
    ATTR_SUCCESS,
    ATTR_DATA_REALKPI,
    ATTR_REALTIME_POWER,
    ATTR_TOTAL_CURRENT_DAY_ENERGY,
    ATTR_TOTAL_CURRENT_MONTH_ENERGY,
    ATTR_TOTAL_LIFETIME_ENERGY,
)


_LOGGER = logging.getLogger(__name__)

class FusionSolarKioksApi:
  
    def getRealTimeKpi(self, username: str, password: str):

        try:
            data = {}
            with PandasClient(user_name=username, system_code=password) as client:
                sl = client.get_station_list()
                station_code = sl['data'][0]['stationCode']
                stationkpi = client.get_station_kpi_real(station_code)
                dl = client.get_dev_list(station_code)
                devkpi = client.get_dev_kpi_real( dl['data'][0]['id'],dl['data'][0]['devTypeId'])
                
                data[ATTR_REALTIME_POWER] = devkpi['data'][0][ATTR_DATA_ITEMMAP]['active_power']

                data[ATTR_TOTAL_CURRENT_DAY_ENERGY] = stationkpi['data'][0][ATTR_DATA_ITEMMAP]['day_power']
                data[ATTR_TOTAL_CURRENT_MONTH_ENERGY] = stationkpi['data'][0][ATTR_DATA_ITEMMAP]['month_power']
                data[ATTR_TOTAL_LIFETIME_ENERGY] = stationkpi['data'][0][ATTR_DATA_ITEMMAP]['total_power']
                _LOGGER.error(devkpi)
                _LOGGER.error(stationkpi)
                _LOGGER.error(data)
                return data
                
            

        except Exception as error:
            _LOGGER.error(error)

    
        return {
            ATTR_SUCCESS: False
        }

class FusionSolarKioskApiError(Exception):
    pass
