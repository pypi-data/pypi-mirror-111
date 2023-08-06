from smart_module.module_system.ID_factions import fac_commoners
from smart_module.module_system.header_game_menus import *
from smart_module.module_system.header_operations import *
from smart_module.module_system.header_skills import *
from smart_module.module_system.header_terrain_types import *
from smart_module.module_system.header_troops import *
from smart_module.module_system.module_constants import *
from smart_module.module_system.module_troops import *
from smart_module.smart_core.utils.pythonUtils import mergeList
from smart_module.smart_modules.base.StringBaseScripts import skill_str_begin

config = {
    ## 收获时间，每4小时收集一次
    "harvestTime":4,
    "survivalTypes":[
        {
            "typeName":"collect_apple",
            "typeNameCn":"采 摘 苹 果",
            "terrains":[rt_forest,rt_mountain_forest,rt_steppe_forest],
            ## 奖励物品
            "reward":"itm_apples",
            ## 最大值100（百分比）
            "probability":30,
            ## 技能增强机率(至少一技能)
            "probabilitySkill": skl_spotting,
            ## 每一个技能增强5%机率
            "probabilitySkillEnhance": 5,
            ## 每次获得数量
            "amount":5,
            ## 技能增强数量
            "amountSkill": skl_looting,
            ## 每一个技能增强10%数量
            "amountSkillEnhance": 10,
            ## 描述信息
            "desc":"每 一 点 侦 察 技 能 增 加 5% 的 机 率 ， 每 一 点 掠 夺 技 能 增 加 10% 的 数 量"
        },
        {
            "typeName":"collect_date_fruit",
            "typeNameCn":"采 摘 枣 子",
            "terrains":[rt_desert_forest],
            ## 奖励物品
            "reward":"itm_raw_date_fruit",
            ## 最大值100（百分比）
            "probability":30,
            ## 技能增强机率(至少一技能)
            "probabilitySkill": skl_spotting,
            ## 每一个技能增强5%机率
            "probabilitySkillEnhance": 5,
            ## 每次获得数量
            "amount":5,
            ## 技能增强数量
            "amountSkill": skl_looting,
            ## 每一个技能增强10%数量
            "amountSkillEnhance": 10,
            ## 描述信息
            "desc":"每 一 点 侦 察 技 能 增 加 5% 的 机 率 ， 每 一 点 掠 夺 技 能 增 加 10% 的 数 量"
        },
        {
            "typeName": "hunt_pig",
            "typeNameCn":"打 猎 野 猪",
            "terrains":[rt_forest,rt_mountain_forest,rt_steppe_forest],
            ## 奖励物品
            "reward": "itm_pork",
            ## 最大值100（百分比）
            "probability": 30,
            ## 技能增强机率
            "probabilitySkill": skl_power_draw,
            ## 每一个技能增强5%机率
            "probabilitySkillEnhance": 5,
            ## 每次获得数量
            "amount": 5,
            ## 技能增强数量
            "amountSkill": skl_looting,
            ## 每一个技能增强10%数量
            "amountSkillEnhance": 10,
            ## 描述信息
            "desc":"每 一 点 侦 察 技 能 增 加 5% 的 机 率 ， 每 一 点 掠 夺 技 能 增 加 10% 的 数 量"
        },
        {
            "typeName": "hunt_fish",
            "typeNameCn":"捕 捞 河 鱼",
            "terrains":[rt_water,rt_river,rt_bridge,rt_snow_forest],
            ## 奖励物品
            "reward": "itm_smoked_fish",
            ## 最大值100（百分比）
            "probability": 30,
            ## 技能增强机率
            "probabilitySkill": skl_power_draw,
            ## 每一个技能增强5%机率
            "probabilitySkillEnhance": 5,
            ## 每次获得数量
            "amount": 5,
            ## 技能增强数量
            "amountSkill": skl_looting,
            ## 每一个技能增强10%数量
            "amountSkillEnhance": 10,
            ## 描述信息
            "desc":"每 一 点 侦 察 技 能 增 加 5% 的 机 率 ， 每 一 点 掠 夺 技 能 增 加 10% 的 数 量"
        },
        {
            "typeName": "fell_wooden_stick",
            "typeNameCn":"砍 伐 树 枝",
            "terrains":[rt_forest,rt_mountain_forest,rt_steppe_forest,rt_snow_forest,rt_desert_forest],
            ## 奖励物品
            "reward": "itm_wooden_stick",
            ## 最大值100（百分比）
            "probability": 30,
            ## 技能增强机率
            "probabilitySkill": skl_power_strike,
            ## 每一个技能增强5%机率
            "probabilitySkillEnhance": 5,
            ## 每次获得数量
            "amount": 20,
            ## 技能增强数量
            "amountSkill": skl_looting,
            ## 每一个技能增强10%数量
            "amountSkillEnhance": 10,
            ## 描述信息
            "desc":"每 一 点 侦 察 技 能 增 加 5% 的 机 率 ， 每 一 点 掠 夺 技 能 增 加 10% 的 数 量"
        },
        {
            "typeName": "mining_stone",
            "typeNameCn":"采 集 石 子",
            ## 限制地形
            "terrains":[rt_mountain,rt_mountain_forest,rt_desert],
            ## 奖励物品
            "reward": "itm_stones",
            ## 最大值100（百分比）
            "probability": 30,
            ## 技能增强机率
            "probabilitySkill": skl_engineer,
            ## 每一个技能增强5%机率
            "probabilitySkillEnhance": 5,
            ## 每次获得数量
            "amount": 20,
            ## 技能增强数量
            "amountSkill": skl_looting,
            ## 每一个技能增强10%数量
            "amountSkillEnhance": 10,
            ## 描述信息
            "desc":"每 一 点 侦 察 技 能 增 加 5% 的 机 率 ， 每 一 点 掠 夺 技 能 增 加 10% 的 数 量"
        },
        {
            "typeName": "collect_grain",
            "typeNameCn":"收 集 野 麦",
            ## 限制地形
            "terrains":[rt_plain],
            ## 奖励物品
            "reward": "itm_grain",
            ## 最大值100（百分比）
            "probability": 10,
            ## 技能增强机率
            "probabilitySkill": skl_spotting,
            ## 每一个技能增强5%机率
            "probabilitySkillEnhance": 5,
            ## 每次获得数量
            "amount": 3,
            ## 技能增强数量
            "amountSkill": skl_looting,
            ## 每一个技能增强10%数量
            "amountSkillEnhance": 10,
            ## 描述信息
            "desc":"每 一 点 侦 察 技 能 增 加 5% 的 机 率 ， 每 一 点 掠 夺 技 能 增 加 10% 的 数 量"
        },
        {
            "typeName": "collect_cabbages",
            "typeNameCn":"收 集 野 菜",
            ## 限制地形
            "terrains":[rt_plain],
            ## 奖励物品
            "reward": "itm_cabbages",
            ## 最大值100（百分比）
            "probability": 10,
            ## 技能增强机率
            "probabilitySkill": skl_spotting,
            ## 每一个技能增强5%机率
            "probabilitySkillEnhance": 5,
            ## 每次获得数量
            "amount": 3,
            ## 技能增强数量
            "amountSkill": skl_looting,
            ## 每一个技能增强10%数量
            "amountSkillEnhance": 10,
            ## 描述信息
            "desc":"每 一 点 侦 察 技 能 增 加 5% 的 机 率 ， 每 一 点 掠 夺 技 能 增 加 10% 的 数 量"
        },
        {
            "typeName": "hunt_hourse",
            "typeNameCn":"驯 服 野 马",
            "terrains":[rt_steppe,rt_steppe_forest],
            ## 奖励物品
            "reward": "itm_steppe_horse",
            ## 最大值100（百分比）
            "probability": 10,
            ## 技能增强机率
            "probabilitySkill": skl_riding,
            ## 每一个技能增强5%机率
            "probabilitySkillEnhance": 2,
            ## 每次获得数量
            "amount": 1,
            ## 技能增强数量
            "amountSkill": skl_looting,
            ## 每一个技能增强10%数量
            "amountSkillEnhance": 10,
            ## 描述信息
            "desc":"每 一 点 侦 察 技 能 增 加 5% 的 机 率 ， 每 一 点 掠 夺 技 能 增 加 10% 的 数 量"
        },
    ]
}



## 收获时间
harvestTime = config.get("harvestTime")
## 测试
# harvestTime = 1


## 初始化survivalTypes
## 1.生成数据保存列表
## 2.生成收集类型字符列表
## 3.生成汉化信息
def initSurvivalTypes():
    ## 汉化列表
    gameStringsList = []
    ## 菜单选项
    gameMenuOptionList = []
    ## 生存类型
    survivalTypes = config.get("survivalTypes")

    for survivalType in survivalTypes:
        ## 生存名称
        typeName = survivalType.get("typeName")
        typeNameCn = survivalType.get("typeNameCn")
        ## 字符串列表 mno_survival_collect
        optionName = "survival_{}".format(typeName)
        optionName_ref = "mno_survival_{}".format(typeName)
        ## 汉化列表
        gameStringsList.append("{}|{}".format(optionName_ref,typeNameCn))

        ## 限制地形
        terrains = survivalType.get("terrains")
        ## 奖励
        reward = survivalType.get("reward")
        ## 机率
        probability = survivalType.get("probability")
        ## 机率所需技能
        probabilitySkill = survivalType.get("probabilitySkill")
        ## 机率所需技能加成
        probabilitySkillEnhance = survivalType.get("probabilitySkillEnhance")
        ## 物品数量
        amount = survivalType.get("amount")
        ## 物品数量所需要技能
        amountSkill = survivalType.get("amountSkill")
        ## 物品数量所需要技能加成
        amountSkillEnhance = survivalType.get("amountSkillEnhance")

        ## 条件
        conditions = []
        conditions.append((party_get_current_terrain,":terrain","p_main_party"))
        for i in range(len(terrains) - 1):
            terrain = terrains[i]
            conditions.append((this_or_next|eq,":terrain",terrain))

        conditions.append((eq, ":terrain", terrains[len(terrains) - 1]))
        ## 结果
        results = []
        results.append((assign,"$g_survival_reward",reward))
        results.append((assign,"$g_survival_probability",probability))
        results.append((assign,"$g_survival_probabilitySkill",probabilitySkill))
        results.append((assign,"$g_survival_probabilitySkillEnhance",probabilitySkillEnhance))
        results.append((assign,"$g_survival_amount",amount))
        results.append((assign,"$g_survival_amountSkill",amountSkill))
        results.append((assign,"$g_survival_amountSkillEnhance",amountSkillEnhance))
        results.append((call_script,"script_start_work_at_wild"))

        gameMenuOptionList.append((optionName,conditions,typeName,results))
    ## 返回
    gameMenuOptionList.append(("go_back", [], "Go back",[(jump_to_menu,"mnu_camp")]))
    return {
        "gameMenuOptionList":gameMenuOptionList,
        "gameStringsList":gameStringsList,
    }


datas = initSurvivalTypes()

gameMenuOptionList = datas.get("gameMenuOptionList")
gameStringsList = datas.get("gameStringsList")

## $g_survival_enable

is_normal = 0 ## 正常
is_working = 1 ## 工作中

pis_workman = 3


WARN_COLOR = 0xfffc9f03


survivalInTheWild={
    "name":"SurvivalInTheWild",
    "enable":True,
    "version": "v2.0.0",
    "desc":'''
        野外生存
            采 摘 苹 果
            采 摘 枣 子
            打 猎 野 猪
            捕 捞 河 鱼
            砍 伐 树 枝
            采 集 石 子
            收 集 野 麦
            收 集 野 菜
            驯 服 野 马
    ''',
    "actions":[
        ("Append@scripts",[
            ("start_work_at_wild",[
                ##(assign,"$g_camp_mode", 1),
                ##(assign, "$g_infinite_camping", 0),
                ##(assign, "$g_player_icon_state", pis_ship),

                (store_skill_level,":probabilitySkillCount","$g_survival_probabilitySkill"),
                (str_store_troop_name,s0,"trp_player"),
                (try_begin),
                    (le,":probabilitySkillCount",0),
                    (store_mul,":strIndex","$g_survival_probabilitySkill",2),
                    (val_add,":strIndex",skill_str_begin),
                    (str_store_string,s1,":strIndex"),
                    (display_message,"@{s0} need skill {s1}",WARN_COLOR),
                (else_try),
                    (assign,"$g_player_icon_state",pis_workman),
                    (rest_for_hours_interactive, 100000, 5, 1), #rest while not attackable
                    (assign,"$g_survival_enable",is_working),
                    (change_screen_return),
                (try_end),
            ]),
        ]),
        ("Append@simple_triggers",[
            (harvestTime,[
                ## 已经开启了野外生存
                (eq,"$g_survival_enable",is_working),
                (store_skill_level,":probabilitySkillCount","$g_survival_probabilitySkill"),
                (str_store_troop_name,s0,"trp_player"),
                (store_mul, ":probabilitySkillEnhance", ":probabilitySkillCount", "$g_survival_probabilitySkillEnhance"),
                ## 获得总机率
                (store_add, ":change", "$g_survival_probability", ":probabilitySkillEnhance"),
                ## 机率最大为100%
                (val_clamp, ":change", 0, 100),
                (store_random_in_range, ":isGet", 0, 100),
                ## 是否成功获得
                (le, ":isGet", ":change"),
                (store_skill_level, ":amountSkillCount", "$g_survival_amountSkill"),
                (store_mul, ":amountSkillEnhance", ":amountSkillCount", "$g_survival_amountSkillEnhance"),
                ## 数量技能增加最100%
                (val_clamp, ":amountSkillEnhance", 0, 100),
                (store_mul, ":plusAmount", "$g_survival_amount", ":amountSkillEnhance"),
                (store_add, ":total", "$g_survival_amount", ":plusAmount"),
                (call_script, "script_get_troop_inventory_free_amount", "trp_player"),
                (assign, ":storageMax", reg0),
                (try_begin),
                    (eq, ":storageMax", 0),
                    (assign, "$g_survival_enable", is_normal),
                    (assign, "$g_player_icon_state", pis_normal),
                    (rest_for_hours, 0, 0, 0),
                    (display_message, "@{s0} storage is full",WARN_COLOR),
                (else_try),
                    (troop_add_items, "trp_player", "$g_survival_reward", ":total"),
                (try_end),
             ]),
            (0,[
                (eq,"$g_survival_enable",is_working),
                (map_free),
                (assign,"$g_survival_enable",is_normal),
                (assign, "$g_player_icon_state", pis_normal),
             ])
        ]),
        ("AddCampOption",[
            ("camp_action_survival_in_the_wild", [], "survival in the wild",
             [
                (jump_to_menu,"mnu_survival_wild"),
             ]
            ),
        ]),
        ("Append@game_menus",[
            ("survival_wild", mnf_disable_all_keys,
             "survival in the wild.",
             "none",
             [],
             gameMenuOptionList
             ),
        ]),
        ("Replace@simple_triggers|#60",[
            (0,[
                (troop_get_inventory_slot, ":cur_horse", "trp_player", 8), #horse slot
                (assign, ":new_icon", -1),
                (try_begin),
                  (eq, "$g_player_icon_state", pis_normal),
                  (try_begin),
                    (ge, ":cur_horse", 0),
                    (assign, ":new_icon", "icon_player_horseman"),
                  (else_try),
                    (assign, ":new_icon", "icon_player"),
                  (try_end),
                (else_try),
                  (eq, "$g_player_icon_state", pis_camping),
                  (assign, ":new_icon", "icon_camp"),
                (else_try),
                  (eq, "$g_player_icon_state", pis_ship),
                  (assign, ":new_icon", "icon_ship"),
                (else_try),
                  (eq, "$g_player_icon_state", pis_workman),
                  (assign, ":new_icon", "icon_axeman"),
                (try_end),
                (neq, ":new_icon", "$g_player_party_icon"),
                (assign, "$g_player_party_icon", ":new_icon"),
                (party_set_icon, "p_main_party", ":new_icon"),
             ])
        ])
    ],
    "internationals":{
            "cns":{
                "game_menus":mergeList(gameStringsList,[
                    "mno_camp_action_survival_in_the_wild|野 外 生 存。",
                    "menu_survival_wild|野 外 生 存 技 能"
                ]),
                "quick_strings":[
                    "qstr_{s0}_need_skill_{s1}|{s0}：我 还 不 会 【{s1}】 技 能",
                    "qstr_{s0}_storage_is_full|{s0}：物 品 栏 已 经 满 了。"
                ]
            }
    }
}