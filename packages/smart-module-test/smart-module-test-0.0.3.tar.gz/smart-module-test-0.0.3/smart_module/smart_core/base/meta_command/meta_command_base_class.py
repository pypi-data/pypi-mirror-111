
################################################
###
### 处理器：命令操作列表
### 方便操作而已
###
################################################
from smart_module.smart_core.base.meta_command.meta_command_grammar_sugar_config import grammarSugarConfig

append = "@Append"
prepend = "@Prepend"
replace = "@Replace"
delete = "@Delete"




gameInitScript = "@GameInitScript"
gameStartMenu = "@GameStartMenu"


if __name__ == '__main__':
    print(grammarSugarConfig)