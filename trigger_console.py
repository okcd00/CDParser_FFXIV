# -*- coding: UTF-8 -*-
# =====================================================
#   Copyright (C) 2016 All rights reserved.
#
#   filename : trigger_consule.py
#   author   : okcd00 / okcd00@qq.com
#   date     : 2020-06-19
#   desc     : for timeline.
# =====================================================
import os
import json
import xmltodict
from pprint import pprint


class Trigger(object):
    def __init__(self, data_str=None):
        self.data = None
        if data_str is not None:
            self.init_data(data_str=data_str)

    def init_data(self, data_str):
        # allow: xml file path, xml string, json string or dict
        if isinstance(data_str, str) and os.path.isfile(data_str):
            with open(data_str, encoding='utf-8') as fp:
                self.data = fp.read()
        elif isinstance(data_str, (str, dict)):
            self.data = data_str

    def xml_to_dict(self, data_str=None):
        if data_str is not None:
            self.init_data(data_str)
        data_ordered = xmltodict.parse(self.data)
        data_json = json.dumps(data_ordered, indent=4)
        data_dict = json.loads(data_json)
        return data_dict

    def to_dict(self, data_str=None):
        return self.xml_to_dict(data_str)

    def dict_to_xml(self, data_str=None):
        if data_str is not None:
            self.init_data(data_str)
        if isinstance(self.data, str):
            self.data = json.loads(self.data)
        return xmltodict.unparse(
            self.data, pretty=True, encoding='gb2312')

    def to_xml(self, data_str=None):
        return self.dict_to_xml(data_str)

    def show_all(self, method='pure'):
        if method == 'dict':
            pprint(self.to_dict())
        elif method == 'xml':
            pprint(self.to_xml())
        else:
            pprint(self.data)


if __name__ == '__main__':
    path = "Triggernometry/TriggernometryExport.xml"
    tl = Trigger(path)
    tl.show_all(method='xml')
