from smart_module.smart_core.base.meta_command.smart_modules_selector import SelectorMatcher
from smart_module.smart_core.smart_modules_log import debug

################################################
###
### 新功能-快捷指令执行器
### 快捷指令：
###     1.指令排序:主要用于基础数据（troops,items,parties,等等）先行固化
###     2.执行指令
###
################################################

class CommandExecutor:

    def __init__(self):
        self.selectorMatcher = SelectorMatcher()
        ## 用于保存命令的列表
        self.commandList = []



    def addCommands(self,commands):
        '''
            排序命令
        :param commandName:
        :return:
        '''
        self.commandList.extend(commands)

    def _sortCommands(self):
        '''
            排序命令
        :return:
        '''
        self.commandList.sort(key=lambda cmd:cmd.level, reverse=False)

    def execCommand(self):
        '''
            运行快速指令
        :param quickCommand:
        :param datas:
        :return:
        '''
        ## 排序指令
        self._sortCommands()
        ## 执行排序后的指令
        for commandInfo in self.commandList:
            commandName = commandInfo.commandName
            target = commandInfo.target
            selector = commandInfo.selector
            processorType = commandInfo.processorType
            moduleInfoStr = commandInfo.moduleInfoStr
            customDatas = commandInfo.customDatas
            datas = commandInfo.datas
            level = commandInfo.level
            ## 实例化处理器
            processor = processorType()
            ## 检索数据获得结果
            debug("[ {} > {} > {} ]: 开始检索数据".format(moduleInfoStr, target, selector))
            selectedResult = self.selectorMatcher.select(datas,selector)
            debug("[ {} > {} > {} ]: 检索数据为，".format(moduleInfoStr, target, selector,selectedResult))
            ## 处理器开始执行
            debug("[ {} > {} > {} ]: 开始执行命令，自定义数据为，{}".format(moduleInfoStr,target, selector,str(customDatas)))
            processor.process(selectedResult,customDatas)
            debug("[ {} > {} > {} ]: 结束执行命令".format(moduleInfoStr, target, selector))



