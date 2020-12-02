import unittest
import os
import json
from datetime import datetime, timedelta
from spaceone.tester import TestCase
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.unittest.result import print_data
from spaceone.core.transaction import Transaction
from spaceone.monitoring.connector.azure_connector import AzureConnector
from spaceone.monitoring.manager.azure_manager import AzureManager
from pprint import pprint

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
    azure_cred = os.environ.get('AZURE_CREDENTIALS')
    test_config = utils.load_yaml_from_file(azure_cred)
    return test_config.get('AZURE_CREDENTIALS', {})


class TestAzureMonitorConnector(TestCase):
    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.monitoring')

        cls.secret_data = _get_credentials()
        cls.azure_connector = AzureConnector(Transaction(), {})
        cls.client = None

        cls.subscription_id = cls.secret_data.get('subscription_id')
        cls.resource_group = 'jhsong-resource-group'
        cls.vm_name = 'jhsong-monitor-test-vm'

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_get_connect_with_azure_secret(self):
        options = {}
        secret_data = self.secret_data
        self.azure_connector.set_connect({}, options, secret_data)

    def test_list_metrics(self):
        options = {}
        secret_data = self.secret_data
        self.azure_connector.set_connect({}, options, secret_data)

        resource_id = f'subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Compute/virtualMachines/{self.vm_name}'
        metrics_info = self.azure_connector.list_metrics(resource_id)
        print(metrics_info)
        print_data(metrics_info, 'test_list_metrics')

    def test_get_metric_data(self):
        end = datetime.utcnow()
        start = end - timedelta(minutes=60*60*7*30)

        options = {}
        secret_data = self.secret_data
        self.azure_connector.set_connect({}, options, secret_data)

        options = {
            'metric': 'Percentage CPU',
            'resource': f'subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Compute/virtualMachines/{self.vm_name}',
            'aligner': 'Total',
            'start': start,
            'end': end,
            'interval': 'PT24H'
        }

        metrics_info = self.azure_connector.get_metric_data(
            options.get('resource'),
            options.get('metric'),
            options.get('start'),
            options.get('end'),
            options.get('interval'),
            options.get('aligner'),
        )

        print_data(metrics_info, 'test_list_metrics')

    def test_all_metric_data(self):
        options = {}
        secret_data = self.secret_data
        self.azure_connector.set_connect({}, options, secret_data)
        resource_id = f'subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Compute/virtualMachines/{self.vm_name}'

        metrics_info = self.azure_connector.list_metrics(resource_id)

        end = datetime.utcnow()
        start = end - timedelta(days=4)

        gcp_mgr = AzureManager()
        period = gcp_mgr._make_period_from_time_range(start, end)
        stat = gcp_mgr._convert_stat('SUM')

        for metric_info in metrics_info:
            metric_data_info = self.azure_connector.get_metric_data(
                resource_id,
                metric_info.name.value,
                start,
                end,
                period,
                stat,
            )
            print_data(metric_data_info, f'test_all_metric_data.{metric_info.name.value}')


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
