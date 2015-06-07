# -*- coding: utf-8 -*-
import json

class getMunis:
    
    def __init__(self, json_file='municipios_municipedia.json'):        
        self.munis = json.load(open(json_file))
