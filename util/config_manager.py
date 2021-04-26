# -*- coding: utf-8 -*-


import json


class Config:

    def __init__(self):
        '''
        init method or constructor
        '''
        self.config = {}

    def system_config(self):
        file_path = "config/system_configuration.json"
        with open(file_path,'r') as config:
            system_configuration = json.load(config)

        return system_configuration

