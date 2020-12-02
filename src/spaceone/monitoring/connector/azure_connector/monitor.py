import logging
import time
from pprint import pprint
from datetime import datetime, timezone
from spaceone.monitoring.error import *

__all__ = ['Monitor']
_LOGGER = logging.getLogger(__name__)


class Monitor(object):

    def __init__(self, client):
        self.client = client

    def list_metrics(self, resource_id):
        return [metric for metric in self.client.metric_definitions.list(resource_id)]

    def get_metric_data(self, resource_id, metric, start, end, period, stat):
        print("-----------")
        print(f'[TIMESPAN] = {start}/{end}')
        print("{}/{}".format(start, end))
        print(f'[INTERVAL] = {period}')
        print("-----------")

        metrics_data = self.client.metrics.list(
            resource_id,
            timespan=f'{start}/{end}',
            interval=period,
            metricnames=metric,
            aggregation=stat
        )

        labels = []
        values = []

        for item in metrics_data.value:
            for timeserie in item.timeseries:
                for data in timeserie.data:
                    labels.append(self._convert_timestamp(data.time_stamp))
                    values.append(self._get_metric_data(getattr(data, stat.lower(), None)))

        return {
            'labels': labels,
            'values': values
        }

    @staticmethod
    def _convert_timestamp(metric_datetime):
        timestamp = int(time.mktime(metric_datetime.timetuple()))
        return {'seconds': timestamp}

    @staticmethod
    def _get_metric_data(metric_value):
        if metric_value:
            return metric_value
        else:
            return 0
