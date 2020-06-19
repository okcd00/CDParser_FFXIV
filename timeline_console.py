# -*- coding: UTF-8 -*-
# =====================================================
#   Copyright (C) 2016 All rights reserved.
#
#   filename : timeline_console.py
#   author   : okcd00 / okcd00@qq.com
#   date     : 2020-06-18
#   desc     : for timeline.
# =====================================================
from pprint import pprint
from xml.dom.minidom import parse, Text, Comment, Element


class TimeLine(object):
    def __init__(self, path=None):
        if path is None:
            path = "timeline/伊甸零式希望乐园 (觉醒篇1).xml"
        self.document_tree = parse(path)
        self.collection = self.document_tree.documentElement

    def to_xml(self):
        return self.collection.toxml()

    @staticmethod
    def get_attr(node, attr='name', end=' | '):
        target = node.getAttributeNode(attr)
        if target:
            print(target.childNodes[0].data, end=end)
            return target.childNodes[0].data
        return None

    def show_all(self):
        phases = self.document_tree.getElementsByTagName("s")
        for phase in phases:
            phase_name = self.get_attr(phase, 'name', end='\n')
            # a_nodes = phase.getElementsByTagName("a")
            # t_nodes = phase.getElementsByTagName("t")
            for line in phase.childNodes:
                if isinstance(line, Text):
                    continue
                elif isinstance(line, Comment):
                    # <!-- comments -->
                    print('# {}'.format(line.data))
                elif isinstance(line, Element):
                    tag_name = line.tagName
                    print('[{}]'.format(tag_name), end=' ')
                    time = self.get_attr(line, 'time')
                    text = self.get_attr(line, 'text')
                    style = self.get_attr(line, 'style')
                    notice = self.get_attr(line, 'notice')
                    sync = self.get_attr(line, 'sync')
                    print("")
                else:
                    print('Uncaught node:', type(line))


if __name__ == '__main__':
    tl = TimeLine(path="timeline/伊甸零式希望乐园 (觉醒篇1).xml")
    tl.show_all()

