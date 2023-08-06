import shareplum.errors
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version

import datetime

import sharelistsync.proxycfg as proxycfg
from sharelistsync.fnsql import fnsql


class SHandler:

    # The init
    def __init__(self, config):
        self.SH = None
        self.LIST = None
        self.config = config
        # Define proxy, if in config
        if "proxy" in config:
            self.set_proxy()

    # Define proxy, if in config
    def set_proxy(self):
        if "proxy" in self.config:
            proxycfg.set_proxy(self.config['proxy'])

    # Connect to sharepoint
    def sharepoint_connect(self):
        authcookie = Office365(self.config['baseurl'],
                               username=self.config['username'],
                               password=self.config['password']
                               ).GetCookies()
        self.SH = Site(self.config['siteurl'], authcookie=authcookie, version=Version.v365)
        return self.SH

    # Get the list resource
    def get_list(self, ret=False):
        try:
            self.LIST = self.SH.List(self.config['listname'])
        except shareplum.errors.ShareplumRequestError:
            if ret:
                return False
            else:
                print('Error retrieving list. The lists available are:')
                self.print_lists()
                raise SystemExit(404)
        return True

    # Get collection of lists and his properties
    def get_lists(self):
        collection = self.SH.GetListCollection()
        return collection

    # Print lists (UUID, Name and link)
    def print_lists(self):
        lists = self.get_lists()
        for list in lists:
            print(list['InternalName'], '=>', list['Title'], 'on', list['DefaultViewUrl'])

    # performs the action defined in the configuration (upload or download)
    def do(self):
        if self.config['mode'] == 'download':
            self.list_download()
        elif self.config['mode'] == 'upload':
            print('Remote sync not implemented yet')
        else:
            raise Exception('Unknown mode')
        return

    # retrieve data from list, truncate stage and load data on it
    def list_download(self):
        viewname = self.config.get("viewnames")
        query = self.config.get("query")
        data = self.LIST.get_list_items(view_name=viewname, query=query)

        sql = fnsql(self.config['mssql'])
        sql.truncate_stage()

        sizes = {}

        for item in data:
            row = {}
            for field in self.config['fields']:
                value = item.get(field)
                if type(value) in (datetime, datetime.date, datetime.datetime, datetime.time):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                row[self.config['fields'][field]] = value

            sql.insert_data(row)
        sql.sync_tables()
