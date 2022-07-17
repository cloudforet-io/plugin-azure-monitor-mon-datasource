import logging
from spaceone.core.service import *
from spaceone.monitoring.manager.azure_manager import AzureManager
from spaceone.monitoring.manager.data_source_manager import DataSourceManager

_LOGGER = logging.getLogger(__name__)
DEFAULT_SCHEMA = 'azure_client_secret'

@authentication_handler
@authorization_handler
@event_handler
class DataSourceService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.azure_mgr: AzureManager = self.locator.get_manager('AzureManager')
        self.data_source_mgr: DataSourceManager = self.locator.get_manager('DataSourceManager')

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        return self.data_source_mgr.init_response()

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """ Verifying data source plugin

        Args:
            params (dict): {
                'schema': 'str',
                'options': 'dict',
                'secret_data': 'dict'
            }

        Returns:
            plugin_verify_response (dict)
        """

        self.azure_mgr.verify(params.get('schema', DEFAULT_SCHEMA), params['options'], params['secret_data'])
