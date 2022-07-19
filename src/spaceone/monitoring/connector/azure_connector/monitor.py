import logging
import time
from pprint import pprint
from spaceone.core import utils
from datetime import datetime, timezone
from spaceone.monitoring.error import *

__all__ = ['Monitor']
_LOGGER = logging.getLogger(__name__)


class Monitor(object):

    def __init__(self, client):
        self.client = client

    def list_metrics(self, resource_id):
        try:
            return [metric for metric in self.client.metric_definitions.list(resource_id)]
        except Exception as e:
            _LOGGER.error(f"[list_metrics]: {e}")
            return []

    def get_metric_data(self, cloud_service_id, resource_id, metric, start, end, period, stat):
        try:
            metrics_data = self.client.metrics.list(
                resource_id,
                timespan=f'{start.strftime("%Y-%m-%dT%H:%M:%S")}/{end.strftime("%Y-%m-%dT%H:%M:%S")}',
                interval=period,
                metricnames=metric,
                aggregation=stat
            )

            labels = []
            value_list = []

            for item in metrics_data.value:
                for timeserie in item.timeseries:
                    for data in timeserie.data:
                        labels.append(self._convert_timestamp(data.time_stamp))
                        value_list.append(self._get_metric_data(getattr(data, stat.lower(), None)))

            return {
                'labels': labels,
                'values': {cloud_service_id: value_list}
            }

        except Exception as e:
            _LOGGER.error(f"[get_metric_data]: {e}")

            return {
                'labels': [],
                'values': {}
            }

    @staticmethod
    def _convert_timestamp(metric_datetime):
        return utils.datetime_to_iso8601(metric_datetime)

    @staticmethod
    def _get_metric_data(metric_value):
        if metric_value:
            return metric_value
        else:
            return 0
