import os
import logging

from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorClient

from spaceone.monitoring.error import *
from spaceone.core.connector import BaseConnector
from spaceone.monitoring.connector.azure_connector.monitor import Monitor

__all__ = ['AzureConnector']
_LOGGER = logging.getLogger(__name__)


class AzureConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monitor_client = None

    def set_connect(self, schema, options: dict, secret_data: dict):
        """
        cred(dict)
            - type: ..
            - tenant_id: ...
            - client_id: ...
            - client_secret: ...
            - subscription_id: ...
        """
        try:
            subscription_id = secret_data['subscription_id']

            os.environ["AZURE_SUBSCRIPTION_ID"] = subscription_id
            os.environ["AZURE_TENANT_ID"] = secret_data['tenant_id']
            os.environ["AZURE_CLIENT_ID"] = secret_data['client_id']
            os.environ["AZURE_CLIENT_SECRET"] = secret_data['client_secret']

            credential = DefaultAzureCredential()

            self.monitor_client = MonitorClient(credential=credential, subscription_id=subscription_id)

        except Exception as e:
            print(e)
            raise ERROR_INVALID_CREDENTIALS(message='connection failed. Please check your authentication information.')

    def list_metrics(self, *args, **kwargs):
        return Monitor(self.monitor_client).list_metrics(*args, **kwargs)

    def get_metric_data(self, *args, **kwargs):
        return Monitor(self.monitor_client).get_metric_data(*args, **kwargs)
