import os

################################################
###
### 显示smart_module的报表信息
### 1.显示编译的概要信息
###
################################################

def reportSmartModule(context):
    configParser = context.configParser
    modules = configParser.getSmartModules()

    print("")
    print("")
    print("编译概要信息")
    print("当前环境：【{}】".format(configParser.getProfile()))
    print("输出目录：{}".format(os.path.abspath(configParser.getExportDir())))
    print("编译数量：{}个模块".format(len(modules)))
    print("==========================================================================================")
    for i in range(len(modules)):
        smartModule = modules[i]
        print("模块编号：{}".format(str(i+1)))
        print("模块名称：{}".format(smartModule.get("name")))
        print("模块版本：{}".format(smartModule.get("version")))
        print("模块简介：{}".format(smartModule.get("desc") if smartModule.get("desc") != None else "无"))
        if i < len(modules) - 1:
            print("------------------------------------------------------------------------------------------")
    print("==========================================================================================")

