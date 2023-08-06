#!/usr/bin/env python3
# coding=utf-8
# ----------------------------------------------------------------------------------------------------
import os
from .yamlconfig import yamlconfig
# ----------------------------------------------------------------------------------------------------
# 类 selfconfig
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2021-05-30 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 未测试 | load_default(self, ...)      | 导入默认配置
# 未测试 | load_by_path(self, ...)      | 导入配置文件
# ----------------------------------------------------------------------------------------------------
class selfconfig(yamlconfig):
    """
    selfconfig类。
    """
    # def __init__(self):
    #     self.server = None
    #     self.client = None
# ----------------------------------------------------------------------------------------------------
    def load_default(self, config_name = 'default.yaml'):
        cata = os.path.dirname(__file__)
        path = os.path.join(cata, config_name)
        self.load_by_path(path)
# ----------------------------------------------------------------------------------------------------
    def load_by_path(self, config_path):
        cfgs = self.yamlload(config_path)
        if 'server' in cfgs:
            if hasattr(self, 'server'):
                print("{0} merge_server:{1}+{2}".format(
                    __name__, self.server, cfgs['server']))
                self.server = self.yamlmerge(self.server, cfgs['server'])
            else:
                self.server = cfgs['server']
                print("{0} server:{1}".format(
                    __name__, self.server))
        if 'client' in cfgs:
            if hasattr(self, 'client'):
                print("{0} merge_client:{1}+{2}".format(
                    __name__, self.client, cfgs['client']))
                self.client = self.yamlmerge(self.client, cfgs['client'])
            else:
                self.client = cfgs['client']
                print("{0} client:{1}".format(
                    __name__, self.client))
# ----------------------------------------------------------------------------------------------------
