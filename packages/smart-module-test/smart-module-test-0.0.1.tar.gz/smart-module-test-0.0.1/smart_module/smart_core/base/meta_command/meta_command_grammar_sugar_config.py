from smart_module.smart_core.base.meta_command.meta_command_processor import AppendProcessor, DeleteProcessor, \
    PrependProcessor, ReplaceProcessor

from smart_module.smart_core.utils.pythonUtils import mergeDict


################################################
###
### 处理器：语法糖，第三部分
### 系统内置语法糖
### 1.正常命令配置：必须提前配置，然后才能使用
###     key:命令名称
###     value:配置参数
###     主要属性：
###     1.【target】: 目标，命令作用在哪个数据集中，如：troops,strings,items,parties等等
###     2.【selector】：选择器，用于选择元素
###     3.【processor】：处理器，选择后，作相应的操作
###     4.【desc】：描述信息，描述命令的作用（可选），建议填写便于理解命令
###
################################################

## 语法糖（命令）合集

grammarSugarConfig = {}


## 通用命令
commonGrammarSugarConfig = {
    "Append":{
        "selector":"#last",
        "processor":AppendProcessor,
        "desc":"用于后置的命令"
    },
    "Prepend":{
        "selector":"#last",
        "processor":PrependProcessor,
        "desc":"用于前置的命令"
    },
    "Replace":{
        "selector":"#last",
        "processor":ReplaceProcessor,
        "desc":"用于替换的命令"
    },
    "Delete":{
        "selector":"#last",
        "processor":DeleteProcessor,
        "desc":"用于删除的命令"
    },
}

## 特殊场景命令
specialGrammarSugarConfig = {
    "GameInitScript":{
        "target":"scripts",
        "selector":"game_start>1>#last",
        "processor":AppendProcessor,
        "desc": "在游戏开始的脚本中增加自定义的语法"
    },
    "GameStartMenu":{
        "target":"game_menus",
        "selector":"start_game_0>5>#first",
        "processor":AppendProcessor,
        "desc": "在游戏开始的菜单中增加自定义的菜单"
    },
    "AppendCustomArrayTroop":{
        "target":"troops",
        "selector":"#last",
        "processor":AppendProcessor,
        "desc": "在游戏开始的脚本中增加自定义的语法"
    },
    "InitWalkers":{
        "target":"scripts",
        "selector":"init_town_walkers>1>#last",
        "processor":AppendProcessor,
        "desc": "访问村庄，城镇时，生成村民或市民，在此指令下，可以自定义自己的人物到村庄或城镇"
    },
    "AddCampOption":{
        "target":"game_menus",
        "selector":"camp>5>camp_action",
        "processor":AppendProcessor,
        "desc": "营地菜单添加新选项"
    },
    "AddDialogForVillage":{
        "target":"dialogs",
        "selector":"village_elder_talk&1:I_want_to_buy_some_supplies%^&3:village_elder_trade_begin&4",
        "processor":PrependProcessor,
        "desc": "为村长增加一个对话"
    }
}

## 合并语法糖集合
grammarSugarConfig = mergeDict(commonGrammarSugarConfig, specialGrammarSugarConfig)
