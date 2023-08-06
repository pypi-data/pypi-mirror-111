from smart_module.smart_core.base.executor.smart_modules_command_executor import CommandExecutor
from smart_module.smart_core.base.executor.smart_modules_quick_command import QuickCommandParser
from smart_module.smart_core.smart_modules_log import info
from smart_module.smart_modules.center.village.VillageBasicBusiness import villageBasicBusiness


################################################
###
### 新功能-SmartModule执行器
### 用于执行actions中的快捷命令
###
################################################

class SmartModuleExecutor:
    def __init__(self):
        self.quickCommandParser = QuickCommandParser()
        self.commandExecutor = CommandExecutor()
        pass

    def collectCommandList(self, smartModule):
        moduleName = smartModule.get("name")
        version = smartModule.get("version")
        enable = smartModule.get("enable")
        moduleInfoStr = "{}（{}）".format(moduleName,version)
        if not enable:
            info("[{}] is disabled".format(moduleInfoStr))
            return
        ## 自定义指令
        customCommands = smartModule.get("commands")

        ## 与剧本相关的数据
        actions = smartModule.get("actions")

        commandList = []
        for action in actions:
            quickCommand = action[0]
            customData = action[1]
            ## 解析命令
            commandInfo = self.quickCommandParser.parseCommand(moduleInfoStr, quickCommand, customCommands, customData)
            commandList.append(commandInfo)
        return commandList



if __name__ == '__main__':
    smartModuleExecutor = SmartModuleExecutor()
    smartModuleExecutor.collectCommandList(villageBasicBusiness)


