import os
import logging
import json


class Configlib:

    def __init__(self, env='prod', config_file='./config/config.env'):
        self.env = env
        self.config_file = config_file
        self.init = False
        self.config_file_list = []
        self.configs = dict()
        pass

    def set_env(self, env='prod'):
        pass

    def get_env(self):
        pass

    def __load_config__(self):
        pass

    def reload_config(self):
        pass

    def get_config_file_names(self):
        # return [self.config_file, 'sftp.json','validate.json','eligibility.json']
        # return self.config_file_list
        pass

    def get_config(self, config_name):
        pass

    def check_config(self,config_name):
        pass

