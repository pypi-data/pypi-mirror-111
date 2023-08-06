## 用于编写一些ai方面的功能
from smart_module.module_system.header_operations import *
from smart_module.module_system.header_parties import *
from smart_module.module_system.module_constants import *

Blank={
    "name":"AiBaseScripts",
    "enable":True,
    "version": "v2.0.0",
    "desc":"这里是描述信息",
    "actions":[
        ("Append@scripts",[
            ## 代码功能
        ]),
        ("Prepend@scripts",[]),
        ("Delete@scripts",[]),
        ("Replace@scripts",[
            ## 集合中只能有一个元素，否则会报错（替换只能精准替换，不能全部替换，而且，只能使用一个数据替换）
        ])
    ],
    ## 汉化
    "internationals":{
            "cns":{
                "dialogs":[

                ]
            }
    }
}