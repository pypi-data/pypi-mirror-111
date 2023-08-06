from smart_module.module_system.header_dialogs import *
from smart_module.module_system.module_scripts import *

'''
    超级功能
    1.招募任何队伍
    2.和同伴对话移动到任何据点附近
'''

superFunction = {
    "name":"SuperFunction",
    "enable":True,
    "version": "v2.0.0",
    "desc":'''
        超级功能
        1.招募任何队伍
        2.和同伴对话移动到任何据点附近
    ''',
    "actions": [
        ("Prepend@dialogs|party_encounter_hostile_defender&1:Nothing%^&3:close_window&4",[
            ## 任何人员加入玩家
            [anyone|plyr, "party_encounter_hostile_defender", [], "I order you to join me.", "super_function_recruit_start", []],
            [anyone, "super_function_recruit_start", [], "yes,my lord!", "close_window", [
                (assign, "$g_leave_encounter",1),
                (call_script,"script_add_party_as_companions","p_main_party","$g_encountered_party",1),
            ]],
        ]),
        ("Prepend@dialogs|lord_talk&1:I_must_beg_my_leave%^&3:lord_leave&4",[
            ## 任何人员加入玩家
            [anyone|plyr, "lord_talk", [], "I order you to join me.", "super_function_recruit_start", []],
            [anyone, "super_function_recruit_start", [], "yes,my lord!", "close_window", [
                (assign, "$g_leave_encounter", 1),
                (call_script,"script_add_party_as_companions","p_main_party","$g_encountered_party",1),
            ]],
        ]),
        ("Prepend@dialogs|member_talk&1:Never_mind_%^&3:close_window&4",[
            ## 任何人员加入玩家
            [anyone|plyr, "member_talk", [], "I want to teleport somewhere.", "super_function_teleport_start", []],
            [anyone, "super_function_teleport_start", [], "What kind of place?", "super_function_teleport_center_type", []],
            [anyone|plyr|repeat_for_100, "super_function_teleport_center_type", [
                (store_repeat_object,":typeIndex"),
                (is_between,":typeIndex",0,4),
                (str_clear,s0),
                (try_begin),
                    (eq,":typeIndex",0),
                    (str_store_string,s0,"@town"),
                (else_try),
                    (eq,":typeIndex",1),
                    (str_store_string,s0,"@castle"),
                (else_try),
                    (eq,":typeIndex",2),
                    (str_store_string,s0,"@village"),
                (else_try),
                    (eq,":typeIndex",3),
                    (str_store_string,s0,"@training_ground_place"),
                (try_end),
            ], "{s0}", "super_function_teleport_center_choice_start", [
                (store_repeat_object,":typeIndex"),
                (str_clear,s0),
                (try_begin),
                    (eq,":typeIndex",0),
                    (assign,"$g_teleport_center_begin",towns_begin),
                    (assign,"$g_teleport_center_end",towns_end),
                    (str_store_string,s0,"@town"),
                (else_try),
                    (eq,":typeIndex",1),
                    (assign, "$g_teleport_center_begin", castles_begin),
                    (assign, "$g_teleport_center_end", castles_end),
                    (str_store_string,s0,"@castle"),
                (else_try),
                    (eq,":typeIndex",2),
                    (assign, "$g_teleport_center_begin", villages_begin),
                    (assign, "$g_teleport_center_end", villages_end),
                    (str_store_string,s0,"@village"),
                (else_try),
                    (eq,":typeIndex",3),
                    (assign, "$g_teleport_center_begin", training_grounds_begin),
                    (assign, "$g_teleport_center_end", training_grounds_end),
                    (str_store_string,s0,"@training_ground_place"),
                (try_end),
            ]],

            [anyone, "super_function_teleport_center_choice_start", [], "{s0}", "super_function_teleport_center_choice_center", []],
            ## 地点选择
            [anyone|plyr|repeat_for_parties, "super_function_teleport_center_choice_center", [
                (store_repeat_object,":centerNo"),
                (is_between,":centerNo","$g_teleport_center_begin","$g_teleport_center_end"),
                (str_store_party_name,s1,":centerNo"),
                (store_faction_of_party,":faction",":centerNo"),
                (str_store_faction_name,s2,":faction"),
            ], "{s0}:{s1}({s2})", "close_window", [
                (store_repeat_object,":centerNo"),
                (party_relocate_near_party,"p_main_party",":centerNo",3),
                (str_store_party_name,s1,":centerNo"),
                (display_message,"@teleport to {s1}"),
            ]],

            [anyone, "super_function_teleport_center_choice_center", [], "no", "close_window", []],

            [anyone, "super_function_teleport_start", [], "nothing.", "close_window", []],
        ]),
    ],
    "internationals":{
        "cns":{
            "dialogs":[
                "dlga_party_encounter_hostile_defender:super_function_recruit_start|【 超 级 功 能 】我 命 令 你 加 入 我 !",
                "dlga_super_function_recruit_start:close_window|好 的 ，大 人 !",
                "dlga_lord_talk:super_function_recruit_start|我 命 令 你 加 入 我 !",
                ## "dlga_super_function_recruit_start:close_window|好 的 ，大 人 !",


                "dlga_member_talk:super_function_teleport_start|【 超 级 功 能 】我 想 传 送 到 某 个 地 方 !",
                "dlga_super_function_teleport_start:super_function_teleport_center_type|什 么 类 型 的 地 方 ？",
            ],
            "quick_strings":[
                "qstr_training_ground_place|训 练 场",
                "qstr_teleport_to_{s1}|传 送 到 : {s1}"
            ]
        }
    },
}