import logging
import time

from spaceone.core.manager import BaseManager
from spaceone.monitoring.error import *
from spaceone.monitoring.connector.azure_connector import AzureConnector

_LOGGER = logging.getLogger(__name__)

_STAT_MAP = {
    'AVERAGE': 'Average',
    'MAX': 'Maximum',
    'MIN': 'Minimum',
    'SUM': 'Total'
}


class AzureManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.azure_connector: AzureConnector = self.locator.get_connector('AzureConnector')

    def verify(self, schema, options, secret_data):
        """ Check connection
        """
        self.azure_connector.set_connect(schema, options, secret_data)

    def set_connector(self, schema, secret_data):
        self.azure_connector.set_connect(schema, {}, secret_data)

    def list_metrics(self, schema, options, secret_data, resource):
        metrics_info = []

        self.azure_connector.set_connect(schema, options, secret_data)

        for metric in self.azure_connector.list_metrics(resource):
            metrics_info.append({
                'key': metric.name.value,
                'name': metric.name.value,
                'unit': {
                    'x': 'Timestamp',
                    'y': metric.unit
                },
                'chart_type': 'line',
                'chart_options': {}
            })

        return {'metrics': metrics_info}

    def get_metric_data(self, schema, options, secret_data, resource, metric, start, end, period, stat):
        if period is None:
            period = self._make_period_from_time_range(start, end)

        stat = self._convert_stat(stat)

        self.azure_connector.set_connect(schema, options, secret_data)
        return self.azure_connector.get_metric_data(resource, metric, start, end, period, stat)

    @staticmethod
    def _convert_stat(stat):
        if stat is None:
            stat = 'AVERAGE'

        if stat not in _STAT_MAP.keys():
            raise ERROR_NOT_SUPPORT_STAT(supported_stat=' | '.join(_STAT_MAP.keys()))

        return _STAT_MAP[stat]

    @staticmethod
    def _make_period_from_time_range(start, end):
        start_time = int(time.mktime(start.timetuple()))
        end_time = int(time.mktime(end.timetuple()))
        time_delta = end_time - start_time

        # Max 60 point in start and end time range
        if time_delta <= 60*60:         # ~ 1h
            return 'PT60S'
        elif time_delta <= 60*60*6:     # 1h ~ 6h
            return 'PT5M'
        elif time_delta <= 60*60*12:    # 6h ~ 12h
            return 'PT15M'
        elif time_delta <= 60*60*24:    # 12h ~ 24h
            return 'PT30M'
        elif time_delta <= 60*60*24*3:  # 1d ~ 2d
            return 'PT1H'
        elif time_delta <= 60*60*24*7:  # 3d ~ 7d
            return 'PT1H'
        elif time_delta <= 60*60*24*14:  # 1w ~ 2w
            return 'PT6H'
        elif time_delta <= 60*60*24*14:  # 2w ~ 4w
            return 'PT12H'
        else:                            # 4w ~
            return 'PT24H'
