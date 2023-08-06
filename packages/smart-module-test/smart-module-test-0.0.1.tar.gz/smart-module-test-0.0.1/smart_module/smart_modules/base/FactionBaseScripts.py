
## 包含一些对阵营常用的操作

## args
from smart_module.module_system.header_common import *
from smart_module.module_system.header_operations import *
from smart_module.module_system.module_constants import *

factionBaseScripts={
    "name":"FactionBaseScripts",
    "enable":True,
    "version": "v2.0.0",
    "desc":"与阵营相关的操作",
    "actions":[
        ("Append@scripts",[
            ## 获得敌国数量
            ("get_num_of_enemy_state",[
                (store_script_param, ":faction_no", 1),
                (assign,":war_num",0),
                (try_for_range,":other_faction_no",kingdoms_begin,kingdoms_end),
                    (neq,":faction_no",":other_faction_no"),
                    (store_relation,":relation",":faction_no",":other_faction_no"),
                    # (assign,reg1,":relation"),
                    # (display_message,"@relation is {reg1}"),
                    (lt,":relation",0),
                    (val_add,":war_num",1),
                (try_end),
                (assign,reg0,":war_num"),
                # (str_store_faction_name, s1, ":faction_no"),
                # (display_message, "@faction({s1}) enemy state nums is {reg0}"),
              ]),
        ])
    ],
}