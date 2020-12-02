import factory

from spaceone.core import utils


class PluginVerifyResponseFactory(factory.DictFactory):

    resource_type = 'monitoring.DataSource'
    actions = []
    result = {
        'options': {
            'supported_resource_type': ['inventory.Server', 'inventory.CloudService'],
            'reference_keys': [{
                'resource_type': 'inventory.Server',
                'reference_key': 'data.azure_monitor'
            }, {
                'resource_type': 'inventory.CloudService',
                'reference_key': 'data.azure_monitor'
            }]
        }
    }
