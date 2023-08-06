
from smart_module.smart_core.banner_print import BannerPrinter
from smart_module.smart_core.base.executor.smart_module_international import SmartModuleLanguageExecutor
from smart_module.smart_core.base.executor.smart_modules_command_executor import CommandExecutor
from smart_module.smart_core.base.executor.smart_modules_runtime import SmartModuleExecutor


################################################
###
### 编译smart_module的主要入口
### 1.编译快捷命令
### 2.汉化
###
################################################
from smart_module.smart_core.smart_modules_log import info
from smart_module.smart_core.utils.DateUtil import DateUtil

def processSmartModule(context):
    modules = context.configParser.getSmartModules()
    bannerPrinter = context.bannerPrinter
    dateUtil = DateUtil()
    dateUtil.start()
    bannerPrinter.print()
    info("【编译】smartModule所有模块")
    ## 编译脚本
    commandExecutor = CommandExecutor()
    smartModuleExecutor = SmartModuleExecutor()
    for smartModule in modules:
        info("【指令收集】开始：{}".format(smartModule["name"]))
        commandList = smartModuleExecutor.collectCommandList(smartModule)
        commandExecutor.addCommands(commandList)
        info("【指令收集】完成：{}".format(smartModule["name"]))
    info("【执行指令】开始")
    commandExecutor.execCommand()
    info("【执行指令】完成")
    info("【编译】完成")

    ## 汉化文件
    smartModuleInternational = SmartModuleLanguageExecutor(context)
    smartModuleInternational.preprocessInternational(modules)

    info("SmartModule模块完成编译！！！")

    ##info("SmartModule模块编译花费时间：{}".format(dateUtil.deltaStr(dateUtil.getAndStart())))
    info("SmartModule模块编译花费时间：{}秒".format(round(dateUtil.getAndStart(),2)))
