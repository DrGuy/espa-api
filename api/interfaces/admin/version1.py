import traceback
import sys
from api.system.logger import ilogger as logger
from api.domain import default_error_message, admin_api_operations


class API(object):
    def __init__(self, providers=None):
        if providers is not None:
            self.providers = providers()
        else:
            from api.interfaces.providers import DefaultProviders
            self.providers = DefaultProviders()

        self.admin = self.providers.administration
        self.reporting = self.providers.reporting
        self.aggregation = self.providers.aggregation

    @staticmethod
    def api_versions():
        """
        Provides list of available api versions

        Returns:
            dict: of api versions and a description

        Example:
            {
                "1":
                    "description": "access points for development",
                }
            }
        """
        resp = dict()
        for version in admin_api_operations['user']:
            resp[version] = admin_api_operations['user'][version]['description']
        return resp

    def access_configuration(self, key=None, value=None, delete=False):
        """
        Provide access to the configuration keys

        :param key: configuration key to match on
        :param value: value to update key to
        :param delete: delete the matching key
        :return: configuration after operation
        """
        try:
            response = self.admin.access_configuration(key=key, value=value, delete=delete)
        except:
            logger.critical('ERR version1 configuration_management:'
                            ' {},{},{}\ntrace: {}\n'.format(key, value, delete,
                                                            traceback.format_exc()))
            response = default_error_message

        return response

    def load_configuration(self, filepath):
        try:
            response = self.admin.restore_configuration(filepath)
        except:
            logger.critical('ERR version1 load_configuration: '
                            '{}\ntrace: {}\n'.format(filepath, traceback.format_exc()))
            response = default_error_message

        return response

    def backup_configuration(self, filepath=None):
        try:
            response = self.admin.backup_configuration(filepath)
        except:
            logger.critical('ERR version1 backup_configuration: '
                            '{}\ntrace: {}\n'.format(filepath, traceback.format_exc()))
            response = default_error_message

        return response

    def get_report(self, name):
        """
        retrieve a named report
        :param name:
        :return: OrderedDict
        """
        try:
            response = str(self.reporting.run(name))
        except:
            logger.critical("ERR version1 get_report name {0}\ntraceback {1}".format(name, traceback.format_exc()))
            response = default_error_message

        return response

    def available_reports(self):
        """
        returns list of available reports
        :return: List
        """
        try:
            response = self.reporting.listing()
        except:
            logger.critical("ERR version1 available_reports traceback {0}".format(traceback.format_exc()))
            response = default_error_message

        return response

    def get_system_status(self):
        """
        retrieve the system status message
        :return: str
        """
        try:
            response = self.admin.get_system_status()
        except:
            logger.critical("ERR version1 get_system_status. traceback {0}".format(traceback.format_exc()))
            response = default_error_message

        return response

    def update_system_status(self, params):
        """
        update system status attributes
        """
        try:
            response = self.admin.update_system_status(params)
        except:
            exc_type, exc_val, exc_trace = sys.exc_info()
            logger.critical("ERR updating system status params: {0}\n exception {1}".format(params, traceback.format_exc()))
            raise exc_type, exc_val, exc_trace

        return response

    def get_system_config(self):
        """
        retrieve system configuration variables
        """
        try:
            return self.admin.get_system_config()
        except:
            exc_type, exc_val, exc_trace = sys.exc_info()
            logger.critical(
                "ERR retrieving system config: exception {0}".format(traceback.format_exc()))
            raise exc_type, exc_val, exc_trace

    def available_stats(self):
        """
        returns list of available statistics
        :return: list
        """
        try:
            response = self.reporting.stat_list()
        except:
            logger.critical("ERR version1 available_stats traceback {0}".format(traceback.format_exc()))
            response = default_error_message

        return response

    def get_stat(self, name):
        """
        retrieve requested statistic value
        :return: long
        """
        try:
            response = self.reporting.get_stat(name)
        except:
            logger.critical("ERR version1 get_stat name: {0}, traceback: {1}".format(name, traceback.format_exc()))
            response = default_error_message
        return response

    def get_multistat(self, name):
        """
        retrieve requested statistic value
        :return: long
        """
        try:
            response = self.reporting.get_multistat(name)
        except:
            logger.critical("ERR version1 get_stat name: {0}, traceback: {1}".format(name, traceback.format_exc()))
            response = default_error_message
        return response

    def get_admin_whitelist(self):
        """
        Returns list of ip addresses for whitelist hosts accessing stats
        :return: list of strings
        """
        try:
            response = self.admin.admin_whitelist()
        except:
            logger.critical("ERR failure to generate web whitelist\ntrace:{}".format(traceback.format_exc()))
            response = default_error_message
        return response

    def get_stat_whitelist(self):
        """
        Returns list of ip addresses for xymon monitoring application accessing stats
        :return: list of strings
        """
        try:
            response = self.admin.stat_whitelist()
        except:
            logger.critical("ERR failure to generate statistics whitelist\ntrace:{}".format(traceback.format_exc()))
            response = default_error_message
        return response

    def error_to(self, orderid, state):
        """
        flip scenes in error for given order to provided state
        :param orderid: order to work with
        :param state: value to set to
        :return: True
        """
        try:
            response = self.admin.error_to(orderid, state)
        except:
            logger.critical("ERR failure to reset to {} error scenes for {}\ntrace: {}".format(state, orderid,
                                                                                            traceback.format_exc()))
            response = default_error_message
        return response

    def get_aux_report(self, group, year):
        """
        get data on gaps in available auxiliary data
        :param group: sensor group, L17 or L8
        :param year: year to report on
        :return: dict of missing days by year
        """
        try:
            response = self.reporting.missing_auxiliary_data(group, year)
        except:
            logger.critical("ERR retrieving auxiliary report for {} group, year {}\ntrace: {}".format(group, year, traceback.format_exc()))
            response = default_error_message
        return response

    def fetch_aggregate_stats(self, aggregation, groupname, data):
        """ Query the database using aggregations.yaml

        :param aggregation: name of aggregation class method
        :param groupname: type of aggregation (orders, scenes, etc)
        :param data: query parameters
        :return: dict
        """
        try:
            response = getattr(self.aggregation, aggregation)(groupname, data)
        except:
            logger.critical("ERR retrieving aggregation report for {} {}: {}\ntrace: {}"
                            .format(aggregation, groupname, data, traceback.format_exc()))
            response = default_error_message
        return response
