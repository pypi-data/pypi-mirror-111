import copy
import re

from smart_module.smart_core.base.exception import SmartModuleExceptin
from smart_module.smart_core.base.meta_command.meta_command_grammar_sugar_config import grammarSugarConfig
from smart_module.smart_core.base.meta_command.module_info_config import moduleDataMaping
from smart_module.smart_core.utils.pythonUtils import mergeDict


################################################
###
### 新功能-快捷指令解析器
### 快捷指令：
###     格式：命令名称@目标|选择器
###     命令必须是之前配置好的，快捷指令只是在已经有的命令上改变一些属性以便让指令适用性更广
###     优先级比较高：
###     1.@：替换target
###     2.|：替换selector
###
################################################

class QuickCommandParser:

    def __init__(self):
        ## 快捷指令格式
        self.quickCommandRegex = "^(\w+)(@(\w+))?(\|(.+))?$"

    def parseQuickCommand(self,quickCommand):
        '''
            解析快捷指令
        :param commandName:
        :return:
        '''
        matcher = re.match(self.quickCommandRegex, quickCommand)
        if not matcher:
            raise SmartModuleExceptin("快捷指令格式错误，请检查：" + quickCommand)
        return (matcher.group(1), matcher.group(3), matcher.group(5))

    def parseCommand(self,moduleInfoStr,quickCommand,customCommands,customDatas):
        '''
            解析命令数据
        :param quickCommand:
        :param datas:
        :return:
        '''
        commandInfo = self.parseQuickCommand(quickCommand)
        commandName = commandInfo[0]
        commandTarget = commandInfo[1]
        commandSelector = commandInfo[2]
        if commandName == None:
            raise SmartModuleExceptin("快捷指令必须提供名称，请检查：" + quickCommand)
        commands = mergeDict(grammarSugarConfig,customCommands if customCommands != None else [])
        buildCommand = commands.get(commandName)
        ## 深度复制，防止修改到内建指令
        command = copy.deepcopy(buildCommand)
        if command == None:
            raise SmartModuleExceptin("未知的快捷指令名称，请检查：" + commandName)
        ## 更新指令信息
        if commandTarget != None:
            command["target"] = commandTarget
        if commandSelector != None:
            command["selector"] = commandSelector
        target = command["target"]
        selector = command["selector"]
        processorType = command["processor"]
        dataConfig = moduleDataMaping.get(target)
        datas = dataConfig["datas"]
        level = dataConfig["level"]
        desc = command["desc"]
        return CommandInfo(commandName,target,selector,processorType,moduleInfoStr,customDatas,datas,level)


class CommandInfo:
    '''
        指令的相关数据
    '''
    def __init__(self,commandName,target,selector,processorType,moduleInfoStr,customDatas,datas,level):
        self.commandName = commandName
        self.target = target
        self.selector = selector
        self.processorType = processorType
        self.moduleInfoStr = moduleInfoStr
        self.customDatas = customDatas
        self.datas = datas
        self.level = level
    def __str__(self):
        return "{}:{}:{}:".format(self.commandName,self.target,self.level)


if __name__ == '__main__':
    quickCommandExecutor = QuickCommandParser()
    print(quickCommandExecutor.parseQuickCommand("Prepend"))
    print(quickCommandExecutor.parseQuickCommand("Prepend@strings"))
    print(quickCommandExecutor.parseQuickCommand("Prepend@strings|village_elder_talk&1:village_elder_trade_begin&4"))


