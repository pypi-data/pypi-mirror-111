import os
import sys

from smart_module.smart_core.base.exception import SmartModuleExceptin


################################################
###
### 配置解析器：解析器
### 1.支持多环境
### 2.提供默认配置
### 3.以后支持命令行（optparse）
###
################################################

class SmartModuleConfigParser:
    def __init__(self,config):
        self.config = config;
        self.profile = self._parseProfile()
        self.environments = self.config.get("environments")
        self.currentConfig = self.environments.get(self.profile)
        if self.currentConfig == None:
            raise SmartModuleExceptin("未找到环境配置，请检查：" + str(self.profile))

    def __str__(self):
        return "smart module 配置解析器"

    def _parseProfile(self):
        ## 环境配置
        profile = self.config.get('profile')

        if profile == None:
            ## 命令行参数
            for arg in sys.argv:
                if arg.startswith("profile="):
                    profile = arg[0:len("profile=")].strip()
                    break;

        if profile == None:
            ## 环境变量
            profile = os.getenv("profile")

        if profile == None:
            ## 如果都没有使用第一个
            environments =  self.config.get("environments")
            (env,config) = environments.items[0]
            profile = env
        return profile

    def getConfig(self,key,default=None):
        value = self.currentConfig.get(key)
        return value if value != None else default

    def getProfile(self):
        '''
            获得输出目录
        :return:
        '''
        return self.profile

    def getExportDir(self):
        '''
            获得输出目录
        :return:
        '''
        return self.getConfig("exportDir")

    def getSrcDir(self):
        '''
            获得源代（Native）码位置
            默认为：module_system
        :return:
        '''
        return self.getConfig("srcDir","./module_system//")

    def getSmartModules(self):
        '''
            获得全部smart模块
        :return:
        '''
        return self.getConfig("smartModules")

    def getSkipNative(self):
        '''
            是否跳过原始（Native）编译
            默认：不跳过
        :return:
        '''
        return self.getConfig("skipNative",False)