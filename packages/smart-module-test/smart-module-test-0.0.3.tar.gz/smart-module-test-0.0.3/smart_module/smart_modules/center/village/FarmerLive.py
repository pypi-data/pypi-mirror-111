## 用于编写一些ai方面的功能
from smart_module.module_system.header_dialogs import *
from smart_module.module_system.header_game_menus import *
from smart_module.module_system.header_operations import *
from smart_module.module_system.header_parties import *
from smart_module.module_system.header_terrain_types import rt_desert
from smart_module.module_system.module_constants import *
from smart_module.smart_core.utils.pythonUtils import mergeList

config = {
    ## 生长变化间隔时间(1月)
    "growInterval":7.2,
    ## 干旱变化间隔时间（1星期）
    "droughtInterval":1.68,
    ## 野草变化间隔时间（2星期）
    "weedInterval":3.36,
    ## 害虫变化间隔时间（2星期）
    "insectInterval":3.36,
    ## 工作变化间隔时间（2星期）
    "workInterval":0.24,
    ## 每过【workInterval】小时，增加健康值【workCount】
    "workCount":1,
    ## 每点【铁骨】技能增加工作进度点数
    "workSkill":skl_ironflesh,
    ## 每点技能增加的点数
    "workSkillCount":1,
    "plants":[
        {
            "plantName":"grain",
            "plantNameCn":"麦 子",
            ## 植物种类
            "plantType":"itm_grain",
            ## 种植费用
            "plantFee":100,
            ## 一块地种植时间（小时）
            "plantTime":2,
            ## 产量 20 * 30 - 100 = 500
            "plantQuantity":20,
        },
        {
            "plantName":"cabbage",
            "plantNameCn":"卷 心 菜",
            ## 植物种类
            "plantType":"itm_cabbages",
            ## 种植费用
            "plantFee":100,
            ## 一块地种植时间（小时）
            "plantTime":2,
            ## 产量 20 * 30 - 100 = 500
            "plantQuantity": 20,
        },
        {
            "plantName":"grape",
            "plantNameCn":"葡 萄",
            ## 植物种类
            "plantType":"itm_raw_grapes",
            ## 种植费用
            "plantFee":150,
            ## 一块地种植时间（小时）
            "plantTime":2,
            ## 产量 10 * 75 - 150 = 600
            "plantQuantity": 10,
        },
        {
            "plantName":"linen",
            "plantNameCn":"亚 麻",
            ## 植物种类
            "plantType":"itm_linen",
            ## 种植费用
            "plantFee":500,
            ## 一块地种植时间（小时）
            "plantTime":5,
            ## 产量 250 * 5 - 500 = 750
            "plantQuantity": 5,
        },
        {
            "plantName":"apple",
            "plantNameCn":"苹 果",
            ## 植物种类
            "plantType":"itm_apples",
            ## 种植费用
            "plantFee":120,
            ## 一块地种植时间（小时）
            "plantTime":5,
            ## 产量 44 * 15 - 120 = 540
            "plantQuantity": 15,
        },
        {
            "plantName":"olive",
            "plantNameCn":"橄 榄",
            ## 植物种类
            "plantType":"itm_raw_olives",
            ## 种植费用
            "plantFee":350,
            ## 一块地种植时间（小时）
            "plantTime":2,
            ## 产量 10 * 100 - 350 = 650
            "plantQuantity": 10,
        },
    ]
}

growInterval = config.get("growInterval")
droughtInterval = config.get("droughtInterval")
weedInterval = config.get("weedInterval")
insectInterval = config.get("insectInterval")

workCount = config.get("workCount")
workInterval = config.get("workInterval")
workSkill = config.get("workSkill")
workSkillCount = config.get("workSkillCount")

plants = config.get("plants")

## 测试状态
# growInterval = 0.1
# droughtInterval = 1
# weedInterval = 1
# insectInterval = 1
# workCount = 3

## $g_farmer_plant_type

## 管理任务模式
## $g_farmer_manage_mode
fmm_none = 1
fmm_planting = 2
fmm_watering = 3
fmm_weeding = 4
fmm_disinsection = 5
fmm_harvest = 6


## $g_farmer_land_planting
## $g_farmer_land_watering
## $g_farmer_land_weeding
## $g_farmer_land_disinsection
## $g_farmer_land_harvest

# $g_farmer_land_process
## 土地未种植
flp_none = 0
## 土地已经种植
flp_planted = 1
## 土地已经成熟
flp_plant_mature = 2
## 土地被毁坏了（洗劫以后）
flp_destroy = 3


# $g_farmer_work_enable
## 休息中
fwe_resting = 0
## 工作中
fwe_working = 1


def initFramerLive():
    plantOptions = []
    plantCnsList = []
    for plant in plants:
        plantName = plant.get("plantName")
        plantNameCn = plant.get("plantNameCn")
        plantType = plant.get("plantType")
        plantFee = plant.get("plantFee")
        plantTime = plant.get("plantTime")
        plantQuantity = plant.get("plantQuantity")

        optionName = "farmer_change_seed_" + plantName
        plantCnsList.append("mno_{}|{}（{}）".format(optionName,plantNameCn,plantFee))
        plantOptions.append((
            optionName,[
                (neg|eq,"$g_farmer_plant_type",plantType),
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
    plantOptions.append(("farmer_change_seed_keep",[], "back",
                 [
                    (jump_to_menu, "mnu_land_manage_options"),
                 ]),)
    plantCnsList.append("mno_farmer_change_seed_keep|保 持 原 样")
    return {
        "plantOptions":plantOptions,
        "plantCnsList":plantCnsList,
    }

datas = initFramerLive()

plantOptions = datas.get("plantOptions")
plantCnsList = datas.get("plantCnsList")

red_color = 0xfffc0303
blue_color = 0xff0300f6
green_color = 0xff49b807

farmerLive={
    "name":"FarmerLive",
    "enable":True,
    "version": "v2.0.0",
    "desc":'''
        村民的生活
            1.定居
            2.管理土地
            3.种植农作物
            4.浇水
            5.除草
            6.除虫
            7.收割
            8.交税
    ''',
    "actions":[
        ("GameInitScript",[
            (assign,"$g_farmer_work_enable",fwe_resting),
            (assign,"$g_farmer_land_process",flp_none),
            (assign,"$g_farmer_manage_mode",fmm_none),

            (assign,"$g_farmer_plant_type",-1),
            (assign,"$g_farmer_plant_fee",-1),
            (assign,"$g_farmer_plant_time",-1),
            (assign,"$g_farmer_plant_quantity",-1),

            (assign,"$g_farmer_land_planting",0),
            (assign,"$g_farmer_land_watering",100),
            (assign,"$g_farmer_land_weeding",100),
            (assign,"$g_farmer_land_disinsection",100),
            (assign,"$g_farmer_land_harvest",0),

        ]),
        ("Append@scripts",[
            ## 开始工作
            ("start_work_at_field",[
                (assign, "$g_farmer_work_enable", fwe_working),
                (rest_for_hours_interactive, 100000, 5, 1),  # rest while not attackable
                (change_screen_return),
            ]),
            # 工作时调用 script_start_work_at_field
            ("update_field_work", [
                ##(assign,"$g_camp_mode", 1),
                ##(assign, "$g_infinite_camping", 0),
                ##(assign, "$g_player_icon_state", pis_ship),

                ## 是否在工作中
                (eq,"$g_farmer_work_enable",fwe_working),

                (store_skill_level, ":workSkill",workSkill,"trp_player"),
                # (assign,reg11,":workSkill"),
                # (display_message,"@workSkillCount {reg11}"),
                (store_mul,":workSkillCount",":workSkill",workSkillCount),
                (str_store_troop_name, s0, "trp_player"),
                ## 默认进度为1
                (assign,":baseCount",workCount),
                (store_add,":plusCount",":workSkillCount",":baseCount"),
                # (assign,reg10,":plusCount"),
                # (display_message,"@plusCount {reg10}"),
                (try_begin),
                    ## 未种植
                    (eq,"$g_farmer_land_process",flp_none),
                    ## 选择种植
                    (eq, "$g_farmer_manage_mode", fmm_planting),
                    (try_begin),
                        (lt,"$g_farmer_land_planting",100),
                        ## 进度增加1
                        (val_add, "$g_farmer_land_planting", ":plusCount"),
                        ## 限制范围0-100
                        (val_clamp,"$g_farmer_land_planting",0,101),
                        (assign,reg0,"$g_farmer_land_planting"),
                        (display_message,"@planting process {reg0}"),
                    (else_try),
                        ## 停止工作
                        (rest_for_hours, 0, 0, 0),
                        (assign,"$g_farmer_work_enable",fwe_resting),
                        (assign,"$g_farmer_land_process",flp_planted),
                        (assign,"$g_farmer_manage_mode",fmm_none),
                        ## 种子费用
                        (troop_remove_gold,"trp_player","$g_farmer_plant_fee"),
                        (display_message, "@{s0} planting is finished",blue_color),
                        ## 种植完成后初始化土地状态
                        (assign,"$g_farmer_land_watering",100),
                        (assign,"$g_farmer_land_weeding",100),
                        (assign,"$g_farmer_land_disinsection",100),
                    (try_end),
                (else_try),
                    ## 已种植
                    (eq,"$g_farmer_land_process",flp_planted),
                    (try_begin),
                        ## 浇水
                        (eq,"$g_farmer_manage_mode",fmm_watering),
                        (try_begin),
                            (lt,"$g_farmer_land_watering",100),
                            ## 进度增加1
                            (val_add, "$g_farmer_land_watering", ":plusCount"),
                            ## 限制范围0-100
                            (val_clamp, "$g_farmer_land_watering", 0, 101),
                            (assign,reg0,"$g_farmer_land_watering"),
                            (display_message,"@watering process {reg0}"),
                        (else_try),
                            (rest_for_hours, 0, 0, 0),
                            (assign,"$g_farmer_work_enable",fwe_resting),
                            (assign,"$g_farmer_manage_mode",fmm_none),
                            (display_message, "@{s0} watering is finished",blue_color),
                            ##(jump_to_menu, "mnu_land_manage_options"),
                        (try_end),
                    (else_try),
                        ## 除草
                        (eq,"$g_farmer_manage_mode",fmm_weeding),
                        (try_begin),
                            (lt,"$g_farmer_land_weeding",100),
                            ## 进度增加1
                            (val_add, "$g_farmer_land_weeding", ":plusCount"),
                            ## 限制范围0-100
                            (val_clamp, "$g_farmer_land_weeding", 0, 101),
                            (assign, reg0, "$g_farmer_land_weeding"),
                            (display_message, "@weeding process {reg0}"),
                        (else_try),
                            (rest_for_hours, 0, 0, 0),
                            (assign,"$g_farmer_work_enable",fwe_resting),
                            (assign,"$g_farmer_manage_mode",fmm_none),
                            (display_message, "@{s0} weeding is finished",blue_color),
                            ##(jump_to_menu, "mnu_land_manage_options"),
                        (try_end),
                    (else_try),
                        ## 除虫
                        (eq,"$g_farmer_manage_mode",fmm_disinsection),
                        (try_begin),
                            (lt,"$g_farmer_land_disinsection",100),
                            ## 进度增加1
                            (val_add, "$g_farmer_land_disinsection", ":plusCount"),
                            ## 限制范围0-100
                            (val_clamp, "$g_farmer_land_disinsection", 0, 101),
                            (assign, reg0, "$g_farmer_land_disinsection"),
                            (display_message, "@disinsection process {reg0}"),
                        (else_try),
                            (rest_for_hours, 0, 0, 0),
                            (assign,"$g_farmer_work_enable",fwe_resting),
                            (assign,"$g_farmer_manage_mode",fmm_none),
                            (display_message, "@{s0} disinsection is finished",blue_color),
                            ##(jump_to_menu, "mnu_land_manage_options"),
                        (try_end),
                    (else_try),
                        (display_message,"@plant has not planted"),
                    (try_end),
                (else_try),
                    ## 已成熟
                    (eq,"$g_farmer_land_process",flp_plant_mature),
                    ## 收割
                    (eq, "$g_farmer_manage_mode", fmm_harvest),
                    (try_begin),
                        (gt,"$g_farmer_land_harvest",0),
                        ## 进度增加1
                        (val_sub, "$g_farmer_land_harvest", ":plusCount"),
                        ## 限制范围0-100
                        (val_clamp, "$g_farmer_land_harvest", 0, 101),
                        (store_sub,":process",100,"$g_farmer_land_harvest"),
                        (assign, reg0, ":process"),
                        (display_message, "@harvest process {reg0}"),
                    (else_try),
                        ## 收获完成
                        (rest_for_hours, 0, 0, 0),
                        (assign,"$g_farmer_work_enable",fwe_resting),
                        (assign,"$g_farmer_land_process",flp_none),
                        (assign,"$g_farmer_manage_mode",fmm_none),
                        (display_message, "@{s0} harvest is finished",blue_color),
                        ## 种植的土地清空
                        (assign,"$g_farmer_land_planting",0),
                        ## 收获物品 ，全部存放到背包，如果超出就直接出售
                        (assign,":baseCount","$g_farmer_plant_quantity"),

                        (assign,":scale","$g_farmer_land_watering"),
                        (val_min,":scale","$g_farmer_land_weeding"),
                        (val_min,":scale","$g_farmer_land_disinsection"),

                        (store_mul,":quantity",":baseCount",":scale"),
                        (val_div,":quantity",100),
                        (troop_add_items,"trp_player","$g_farmer_plant_type",":quantity"),
                        ##(jump_to_menu, "mnu_land_manage_options"),
                    (try_end),
                (else_try),
                    ## 土地已销毁
                    (eq,"$g_farmer_land_process",flp_destroy),
                    (assign,":continue",0),
                (try_end),
            ]),
        ]),
        ("Append@simple_triggers",[
            ## 庄家生长（100：代表可以收获了）
            (growInterval,[
                (eq,"$g_farmer_land_process",flp_planted),
                (try_begin),
                    (lt,"$g_farmer_land_harvest",100),
                    (val_add,"$g_farmer_land_harvest",1),
                    (val_clamp,"$g_farmer_land_harvest",0,101),
                (else_try),
                    ## 农作物成熟了
                    (assign,"$g_farmer_land_process",flp_plant_mature),
                    (display_message,"@farmer plant is matured",green_color),
                (try_end),
            ]),
            ## 土地干涸（100：不缺水）
            (droughtInterval,[
                (eq,"$g_farmer_land_process",flp_planted),
                ## 没有人管理时
                (eq, "$g_farmer_manage_mode", fmm_none),
                (try_begin),
                    (gt,"$g_farmer_land_watering",0),
                    (val_sub,"$g_farmer_land_watering",1),
                    (val_clamp,"$g_farmer_land_watering",0,101),
                (else_try),
                    ## 农作物干涸死了
                    (assign,"$g_farmer_land_process",flp_none),
                    ## 清空农作物
                    (assign,"$g_farmer_land_planting",0),
                    ## 清空可收获农作物
                    (assign,"$g_farmer_land_harvest",0),
                    (display_message,"@farmer plant dry to death",red_color),
                (try_end),
            ]),
            ## 土地野草生长（100：没有杂草）
            (weedInterval,[
                ## 农作物已经种植
                (eq, "$g_farmer_land_process", flp_planted),
                ## 没有人管理时
                (eq, "$g_farmer_manage_mode", fmm_none),
                (try_begin),
                    (gt, "$g_farmer_land_weeding", 0),
                    (val_sub, "$g_farmer_land_weeding", 1),
                    (val_clamp, "$g_farmer_land_weeding", 0, 101),
                (else_try),
                    ## 农作物被野草淹没
                    (assign, "$g_farmer_land_process", flp_none),
                    ## 清空农作物
                    (assign, "$g_farmer_land_planting", 0),
                    ## 清空可收获农作物
                    (assign,"$g_farmer_land_harvest",0),
                    (display_message, "@farmer plant are submerged by weeds",red_color),
                (try_end),
            ]),
            ## 土地实害虫生长（100：没有虫子）
            (weedInterval,[
                (eq, "$g_farmer_land_process", flp_planted),
                ## 没有人管理时
                (eq, "$g_farmer_manage_mode", fmm_none),
                (try_begin),
                    (gt, "$g_farmer_land_disinsection", 0),
                    (val_sub, "$g_farmer_land_disinsection", 1),
                    (val_clamp, "$g_farmer_land_disinsection", 0, 101),
                (else_try),
                    ## 农作物被虫子吃完了
                    (assign, "$g_farmer_land_process", flp_none),
                    ## 清空农作物
                    (assign, "$g_farmer_land_planting", 0),
                    ## 清空可收获农作物
                    (assign,"$g_farmer_land_harvest",0),
                    (display_message, "@farmer plant were eaten up by insects",red_color),
                (try_end),
            ]),
            ## 玩家主动停止工作
            (0,[
                ## 如果在工作中
                (eq,"$g_farmer_work_enable",fwe_working),
                (map_free),
                (assign,"$g_farmer_work_enable",fwe_resting),
                (display_message,"@farmer stop work"),
             ]),
            ## 更新土地状态（野草，干旱，等等）
            (workInterval,[
                ## 如果在工作中
                (call_script,"script_update_field_work"),
             ])
        ]),
        ("AddDialogForVillage",[
            [anyone | plyr, "village_elder_talk", [], "I want to settle here.",
             "talk_elder_tobe_farmer_start", [
             ]],

            ## 同意加入
            [anyone, "talk_elder_tobe_farmer_start", [
                (troop_slot_eq,"trp_player",slot_troop_home,0),
            ], "Welcome to join us and do well.",
             "close_window", [
                ## 定居
                (troop_set_slot,"trp_player",slot_troop_home,"$current_town"),
                 (str_store_party_name,s0,"$current_town"),
                 (party_set_extra_text,"p_main_party","@{s0}'s farmer"),
             ]],

            ## 已经是别的村民
            [anyone, "talk_elder_tobe_farmer_start", [
                (neg|troop_slot_eq,"trp_player",slot_troop_home,0),
                (neg|troop_slot_eq,"trp_player",slot_troop_home,"$current_town"),
            ], "Sory,You are already a villager in another village!",
             "close_window", []],

            ## 已经是本村村民
            [anyone, "talk_elder_tobe_farmer_start", [
                (neg|troop_slot_eq,"trp_player",slot_troop_home,0),
                (troop_slot_eq,"trp_player",slot_troop_home,"$current_town"),
            ], "You are already a villager of the village.",
             "close_window", []],
        ]),
        ## 如果是村民，就拥有一块可以自己管理的土地
        ("Append@game_menus|village>5>village_manage",[
            ("land_manage",
             [
                 ## 玩家的家乡是当前村庄
                 (troop_slot_eq,"trp_player",slot_troop_home,"$current_town")
             ]
             , "Manage your land.",
             [
                 (jump_to_menu, "mnu_land_manage_options"),
             ]),
        ]),

        ## 不能打劫自己村庄
        ("Append@game_menus|village>5>village_hostile_action>1>#last",[
            (neg|troop_slot_eq,"trp_player",slot_troop_home,"$current_town"),
        ]),
        ## 能在村庄休息
        ("Append@game_menus|village>5>village_wait",[
            ("village_wait",
               [
                   (assign,":townLord","0"),
                   (try_begin),
                        (party_slot_eq, "$current_town", slot_center_has_manor, 1),
                        (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
                        (assign, ":townLord", "1"),
                   (try_end),
                    (this_or_next|troop_slot_eq,"trp_player",slot_troop_home,"$current_town"),
                   (eq,":townLord",1),

                ],
                 "Wait here for some time.",
                 [
                   (assign,"$auto_enter_town","$current_town"),
                   (assign, "$g_last_rest_center", "$current_town"),

                   (try_begin),
                     (party_is_active, "p_main_party"),
                     (party_get_current_terrain, ":cur_terrain", "p_main_party"),
                     (try_begin),
                       (eq, ":cur_terrain", rt_desert),
                       (unlock_achievement, ACHIEVEMENT_SARRANIDIAN_NIGHTS),
                     (try_end),
                   (try_end),
                   (rest_for_hours_interactive, 24 * 7, 5, 1), #rest while attackable
                   (change_screen_return),
          ]),

        ]),
        ("Append@game_menus",[
            ("land_manage_options", mnf_disable_all_keys,"Take good care of your land, and you will get rich rewards.","none",
             [],[
                ## 更换种子
                ("farmer_change_seed",[
                    ## (eq,"$g_farmer_plant_type",-1),
                ], "change seed",
                 [
                     (try_begin),
                        (eq,"$g_farmer_land_process",flp_none),
                        (assign, "$g_farmer_manage_mode", "mnu_village"),
                        (jump_to_menu, "mnu_farmer_change_seed_list"),
                    (else_try),
                        (eq, "$g_farmer_land_process", flp_planted),
                        (display_message,"@farmer is planted!"),
                    (else_try),
                        (eq, "$g_farmer_land_process", flp_plant_mature),
                        (display_message,"@farmer plant is matured"),
                    (else_try),
                        (eq, "$g_farmer_land_process", flp_destroy),
                        (display_message,"@farmer is destroyed!"),
                    (try_end),
                 ]),
                ## 种植
                ("farmer_plant_seed",[
                    (gt,"$g_farmer_plant_type",0),
                    (assign,reg0,"$g_farmer_land_planting"),
                ], "planting({reg0})",
                 [
                     (try_begin),
                        (eq,"$g_farmer_land_process",flp_none),
                        (assign, "$g_farmer_manage_mode",fmm_planting),
                        (call_script,"script_start_work_at_field"),
                     (else_try),
                        (display_message,"@framer land is not free"),
                     (try_end),
                 ]),
                ## 浇水
                ("farmer_watering",[
                    (eq,"$g_farmer_land_process",flp_planted),
                    (lt,"$g_farmer_land_watering",100),
                    (assign,reg1,"$g_farmer_land_watering"),
                ], "watering({reg1})",
                 [
                     (assign, "$g_farmer_manage_mode", fmm_watering),
                     (call_script, "script_start_work_at_field"),
                 ]),
                ## 除草
                ("farmer_weeding",[
                    (eq, "$g_farmer_land_process", flp_planted),
                    (lt, "$g_farmer_land_weeding", 100),
                    (assign, reg2, "$g_farmer_land_weeding"),
                ], "weeding({reg2})",
                 [
                     (assign, "$g_farmer_manage_mode", fmm_weeding),
                     (call_script, "script_start_work_at_field"),
                 ]),
                ## 除虫
                ("farmer_disinsection",[
                    (eq, "$g_farmer_land_process", flp_planted),
                    (lt, "$g_farmer_land_disinsection", 100),
                    (assign, reg3, "$g_farmer_land_disinsection"),
                ], "disinsection({reg3})",
                 [
                     (assign, "$g_farmer_manage_mode", fmm_disinsection),
                     (call_script, "script_start_work_at_field"),
                 ]),
                ## 收割
                ("farmer_harvest",[
                    (assign, reg4, "$g_farmer_land_harvest"),
                ], "harvest({reg4})",
                 [
                    (try_begin),
                        (eq,"$g_farmer_land_process",flp_plant_mature),
                        (assign, "$g_farmer_manage_mode",fmm_harvest),
                        (call_script, "script_start_work_at_field"),
                    (else_try),
                        (eq,"$g_farmer_land_process",flp_none),
                        (display_message,"@framer land is not planted"),
                    (else_try),
                        (display_message,"@plant is not mature"),
                    (try_end),
                 ]),
                ## 收割
                ("farmer_back",[], "back",
                 [
                    (jump_to_menu, "mnu_village"),
                 ]),
             ]),

            ## 切换种植类型
            ("farmer_change_seed_list", mnf_disable_all_keys,"Please choose the type you want to plant.","none",[],plantOptions),
        ]),
    ],
    ## 汉化
    "internationals":{
            "cns":{
                "game_menus":mergeList(plantCnsList,[
                    "mno_land_manage|管 理 你 的 土 地。",
                    "menu_land_manage_options|好 好 管 理 你 的 土 地 ， 你 会 得 到 丰 厚 的 回 报。",
                    "menu_farmer_change_seed_list|请 选 择 一 个 你 想 要 种 植 的 农 作 物 。",
                    "mno_farmer_change_seed|更 换 庄 家 种 类。",
                    "mno_farmer_plant_seed|开 始 种 植 （{reg0}）",
                    "mno_farmer_watering|开 始 浇 水 （{reg1}）",
                    "mno_farmer_weeding|开 始 除 草 （{reg2}）",
                    "mno_farmer_disinsection|开 始 除 虫 （{reg3}）",
                    "mno_farmer_harvest|开 始 收 获 （{reg4}）",
                    "mno_farmer_back|返 回",
                ]),
                "dialogs":[
                    "dlga_village_elder_talk:talk_elder_tobe_farmer_start|我 想 定 居 在 这 个 村 庄 。",
                    "dlga_talk_elder_tobe_farmer_start:close_window|欢 迎 加 入 我 们 ，好 好 干 。",
                    "dlga_talk_elder_tobe_farmer_start:close_window.1|对 不 起 ，你 已 经 加 入 别 的 村 庄 。",
                    "dlga_talk_elder_tobe_farmer_start:close_window.2|你 已 经 是 我 们 村 的 村 民 。",
                ],
                "quick_strings":[
                    "qstr_farmer_change_{s0}|更 改 家 作 物 类 型 为 {s0}",
                    "qstr_planting_process_{reg0}|种 植 进 度 ：{reg0}%",
                    "qstr_{s0}_planting_is_finished|{s0}：种 植 完 成 ！",
                    "qstr_watering_process_{reg0}|浇 水 进 度 ：{reg0}%",
                    "qstr_{s0}_watering_is_finished|{s0}：浇 水 完 成 ！",
                    "qstr_weeding_process_{reg0}|除 草 进 度 ：{reg0}%",
                    "qstr_{s0}_weeding_is_finished|{s0}：除 草 完 成 ！",
                    "qstr_disinsection_process_{reg0}|除 虫 进 度 ：{reg0}%",
                    "qstr_{s0}_disinsection_is_finished|{s0}：除 虫 完 成 ！",
                    "qstr_harvest_process_{reg0}|收 获 进 度 ：{reg0}%",
                    "qstr_{s0}_harvest_is_finished|{s0}：收 获 完 成 ！",
                    "qstr_farmer_stop_work|停 止 工 作 ！",
                    "qstr_farmer_is_planted_|农 作 物 已 经 种 植 了 ！",
                    "qstr_farmer_is_destroyed_|土 地 被 烧 毁 了 ！",
                    "qstr_farmer_plant_is_matured|家 作 物 成 熟 了 ！",
                    "qstr_plant_is_not_mature|家 作 物 还 没 有 成 熟 ！",

                    "qstr_framer_land_is_not_free|土 地 当 前 不 是 空 闲 的 ！",
                    "qstr_framer_land_is_not_planted|土 地 还 没 有 种 植 任 何 农 作 物 ！",

                    "qstr_farmer_plant_dry_to_death|农 作 物 已 经 干 旱 死 亡 ！",
                    "qstr_farmer_plant_are_submerged_by_weeds|农 作 物 已 经 杂 草 吞 噬 ！",
                    "qstr_farmer_plant_were_eaten_up_by_insects|农 作 物 已 经 害 虫 吃 完 ！",

                    "qstr_{s0}_s_farmer|{s0}的 村 民",
                ]
            }
    }
}