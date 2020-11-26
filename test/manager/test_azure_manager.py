import os
import json
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.monitoring.error import *
from spaceone.monitoring.connector.azure_connector import AzureConnector
from spaceone.monitoring.manager.azure_manager import AzureManager


AZURE_CREDENTIALS_PATH = os.environ.get('AZURE_CREDENTIALS', None)

if AZURE_CREDENTIALS_PATH is None:
    print("""
        ##################################################
        # ERROR 
        #
        # Configure your Azure credential first for test
        #
        ##################################################
        example)

        export AZURE_CREDENTIALS="<PATH>" 
    """)
    exit

def _get_credentials():
    with open(AZURE_CREDENTIALS_PATH) as json_file:
        json_data = json.load(json_file)
        return json_data

class TestMetricManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.monitoring')

        cls.secret_data = _get_credentials() if _get_credentials() is not None else {}
        cls.subscription_id = cls.secret_data.get('subscription_id')
        cls.resource_group = 'cloudone-test'
        cls.vm_name = 'jhsong'

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    @patch.object(AzureConnector, '__init__', return_value=None)
    def test_convert_stat(self, *args):
        azure_mgr = AzureManager()
        stat = azure_mgr._convert_stat('AVERAGE')
        print_data(stat, 'test_convert_stat')

    @patch.object(AzureConnector, '__init__', return_value=None)
    def test_convert_stat_with_invalid_stat(self, *args):
        azure_mgr = AzureManager()
        with self.assertRaises(ERROR_NOT_SUPPORT_STAT):
            azure_mgr._convert_stat('MEAN')

    @patch.object(AzureConnector, '__init__', return_value=None)
    def test_make_period_from_time_range(self, *args):
        azure_mgr = AzureManager()

        end = datetime.utcnow()
        start = end - timedelta(days=1)

        period = azure_mgr._make_period_from_time_range(start, end)
        print_data(period, 'test_make_period_from_time_range')

    @patch.object(AzureConnector, '__init__', return_value=None)
    def test_get_metric_data(self, *args):
        schema = 'azure_client_secret'

        azure_mgr = AzureManager()
        metric = 'Percentage CPU'
        resource = f'subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Compute/virtualMachines/{self.vm_name}'
        stat = 'AVERAGE'
        options = {}
        end = datetime.utcnow()
        start = end - timedelta(days=2)
        period = azure_mgr._make_period_from_time_range(start, end)

        azure_mgr.get_metric_data(schema, options, self.secret_data, resource, metric, start, end, period, stat)
        print_data(period, 'test_make_period_from_time_range')

if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
