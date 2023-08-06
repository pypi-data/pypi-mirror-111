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
    ## 进度更新时间
    "updateTime":0.25,
    "skill":skl_engineer,
    ## 图纸列表
    "blueprintList":[
        {
            "typeName":"dagger",
            "typeNameCn":"匕 首",
            "reward":"itm_dagger",
            ## 制作最低【工程师】级别
            "skillLevel":1,
            ## 制作花费时间
            "makeCostTime":2,
            ## 制作花费的金额
            "makeCostMoney":10,
            ## 学习如何制作花费的时间
            "learnCostTime":2,
            ## 学习到的机率（100:代表一定学会）
            "learnProbability":100,
            "materialList":[
                {
                    "material":"itm_iron",
                    "amount":1
                },
                {
                    "material":"itm_wooden_stick",
                    "amount":1
                },
            ],
            ## 描述信息
            "desc":"最简单的图纸"
        },
    ]
}



## 收获时间
updateTime = config.get("updateTime")
skill = config.get("skill")
blueprintList = config.get("blueprintList")
## 测试
updateTime = 1


systemBlueprintList = "trp_system_blueprint_list"
playerBlueprintList = "trp_player_blueprint_list"

def initHandicraftIndustry():
    ## 图纸列表
    blueprintMenusList = []
    ## 图纸选项列表
    blueprintMenusOptions = []
    blueprintCnsList = []
    blueprintCommandList = []
    for index in range(len(blueprintList)):
        blueprint = blueprintList[index]
        typeName = blueprint.get("typeName")
        plantNameCn = blueprint.get("plantNameCn")
        reward = blueprint.get("reward")
        skillLevel = blueprint.get("skillLevel")
        makeCostTime = blueprint.get("makeCostTime")
        makeCostMoney = blueprint.get("makeCostMoney")
        learnCostTime = blueprint.get("learnCostTime")
        learnProbability = blueprint.get("learnProbability")
        materialList = blueprint.get("materialList")

        ## 保存系统蓝图的列表
        blueprintCommandList.append((troop_set_slot,systemBlueprintList,index,reward))


        optionName = "handicraft_" + typeName
        blueprintCnsList.append("mno_{}|{}（{}）".format(optionName,plantNameCn,skillLevel))
        blueprintOptions.append((
            optionName,[
                ## 玩家已经学会
                (neg|eq,"$g_farmer_plant_type",plantType),
                ## 玩家级别超过限制
                (store_skill_level, ":skillCount", skill),
                (ge,":skillCount",skillLevel),
            ], plantName,[
                (eq, "$g_farmer_land_process", flp_none),
                (assign, "$g_farmer_plant_type", plantType),
                (assign, "$g_farmer_plant_fee", plantFee),
                (assign, "$g_farmer_plant_time", plantTime),
                (assign, "$g_farmer_plant_quantity", plantQuantity),
                (str_store_item_name,s0,plantType),
                (display_message, "@farmer change {s0}"),
                ## 切换到上一层菜单
                (jump_to_menu, "mnu_land_manage_options"),
            ]
        ))
    blueprintOptions.append(("farmer_change_seed_keep",[], "back",
                 [
                    (jump_to_menu, "mnu_land_manage_options"),
                 ]),)
    blueprintCnsList.append("mno_farmer_change_seed_keep|返 回")
    return {
        "plantOptions":plantOptions,
        "plantCnsList":plantCnsList,
    }


datas = initHandicraftIndustry()

gameMenuOptionList = datas.get("gameMenuOptionList")
gameStringsList = datas.get("gameStringsList")

## $g_survival_enable

is_normal = 0 ## 正常
is_working = 1 ## 工作中

pis_workman = 3


WARN_COLOR = 0xfffc9f03


handicraftIndustry={
    "name":"HandicraftIndustry",
    "enable":True,
    "version": "v2.0.0",
    "desc":'''
        打造系统
            可以手工打造一些物品
            1.匕首
    ''',
    "actions":[
        ("AppendCustomArrayTroop",[
            ## 用于保存所有的蓝图列表
            ["system_blueprint_list", "system blueprint list", "system blueprint list", tf_hero, no_scene, reserved, fac_commoners, [],
             def_attrib, 0, knows_common | knows_inventory_management_10, 0],
            ## 用于保存玩家学会的蓝图列表（会：1，不会：0）
            ["player_blueprint_list", "player blueprint list", "player blueprint list", tf_hero, no_scene, reserved, fac_commoners, [],
             def_attrib, 0, knows_common | knows_inventory_management_10, 0],
        ]),
        ## 在营地增加一个选项
        ("AddCampOption",[
            ("camp_action_open_blueprint_list", [], "open blueprint list",
             [
                (jump_to_menu,"mnu_blueprint_list"),
             ]
            ),
        ]),
        ("Append@game_menus",[
            ## 图纸列表
            ("blueprint_list", mnf_disable_all_keys,
             "blueprint list",
             "none",
             [],
             gameMenuOptionList
             ),
            ## 图纸选项组
            ("blueprint_options", mnf_disable_all_keys,
             "blueprint options",
             "none",
             [],
             gameMenuOptionList
             ),
        ]),





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