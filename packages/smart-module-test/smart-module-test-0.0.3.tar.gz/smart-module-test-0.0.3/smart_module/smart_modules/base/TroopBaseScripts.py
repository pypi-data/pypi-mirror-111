
## 包含一些对兵种常用的操作

## 姓氏
from smart_module.module_system.header_operations import *
from smart_module.module_system.header_parties import *
from smart_module.module_system.header_skills import *
from smart_module.module_system.module_constants import *
from smart_module.smart_core.utils.pythonUtils import *
from smart_module.smart_core.smart_module_slot import smartModuleSlotManager

first = ["陈","李","黄","张","朱","梁","林","刘","马","白","吴","曹","蔡","车","谭","罗","杨","诸 葛","司 马","南 宫","太 史","公 良","公 孙","公 良","百 里"]
## 名字
second = ["宛","丘","形","采","用","其","利","器","用","桐","平","桃","山","明","月","朋","峰","峦","清","浮","桥","杰","贡","英","弄","三","武","言","玄 策","大 目","三 刀"]


def parseFirstStrings(chars):
    list = []
    for index in range(len(chars)):
        list.append(("first_name_{}".format(index),"{}".format(chars[index])))
    list.append(("first_name_end","end"))
    return list

def parseSecondStrings(chars):
    list = []
    for index in range(len(chars)):
        list.append(("second_name_{}".format(index),"{}".format(chars[index])))
    list.append(("second_name_end","end"))
    return list

def parseCnsFirstStrings(chars):
    list = []
    for index in range(len(chars)):
        list.append("str_first_name_{}|{}".format(index,chars[index]))
    return list

def parseCnsSecondStrings(chars):
    list = []
    for index in range(len(chars)):
        list.append("str_second_name_{}|{}".format(index,chars[index]))
    return list

first_begin = "str_first_name_0"
first_end = "str_first_name_end"

second_begin = "str_second_name_0"
second_end = "str_second_name_end"



## slot
slot_troop_first_name = smartModuleSlotManager.getTroopSlotNo("slot_troop_first_name")
slot_troop_second_name = smartModuleSlotManager.getTroopSlotNo("slot_troop_second_name")

troopBaseScripts={
    "name":"TroopBaseScripts",
    "enable":True,
    "version": "v2.0.0",
    "desc":"与人物或兵种相关的操作",
    "actions": [
        ("Append@scripts",[
            ## 出门
            ("troop_leave_home",[
                (store_script_param, ":troop", 1),
                (troop_get_slot,":home",":troop",slot_troop_cur_center),
                (party_get_slot, ":home_castle", ":home", slot_town_castle),
                (remove_troop_from_site, ":troop",":home_castle"),
                ##(display_message,"str_s5_leave_home"),
              ]),
            ## 回家
            ("troop_go_home",[
                (store_script_param, ":troop", 1),
                (troop_get_slot,":home",":troop",slot_troop_cur_center),
                (party_get_slot, ":home_castle", ":home", slot_town_castle),
                (modify_visitors_at_site, ":troop",":home_castle"),
                ##(display_message,"str_s5_go_home"),
              ]),

            ("set_random_name",[
                (store_script_param_1,":troop"),
                (store_random_in_range,":first",first_begin,first_end),
                (store_random_in_range,":second",second_begin,second_end),
                (troop_set_slot,":troop",slot_troop_first_name,":first"),
                (troop_set_slot,":troop",slot_troop_second_name,":second"),
                (str_store_string,s1,":first"),
                (str_store_string,s2,":second"),
                (troop_set_name,":troop","str_s1_s2_name"),
            ]),
            ("get_random_first_name",[
                (store_random_in_range,":first",first_begin,first_end),
                (assign,reg0,":first"),
            ]),
            ("get_random_second_name", [
                (store_random_in_range, ":second", second_begin, second_end),
                (assign,reg0,":second"),
            ]),

            ("set_name_for_son", [
                (store_script_param_1, ":father"),
                (store_script_param_2, ":son"),

                (str_store_troop_name,s3,":father"),

                (troop_get_slot,":first_name",":father",slot_troop_first_name),

                (assign,reg1,":first_name"),
                (display_message,"@father first name id {reg1}"),


                (call_script,"script_get_random_second_name"),
                (assign,":second_name",reg0),

                (troop_set_slot,":son",slot_troop_first_name,":first_name"),
                (troop_set_slot,":son",slot_troop_second_name,":second_name"),

                (str_store_string, s1, ":first_name"),
                (str_store_string, s2, ":second_name"),
                (troop_set_name, ":son", "str_s1_s2_name"),

                (troop_set_slot, ":son", slot_troop_father, ":father"),


                (display_message,"@son(father:{s3}) first name:{s1}  second name:{s2}"),
            ]),
            ("display_troop_info",[
                (store_script_param_1,":troop"),
                ## 姓名
                (str_store_troop_name,s1,":troop"),
                (display_message,"@name:{s1}"),
                ## 姓
                (troop_get_slot,":first_name",":troop",slot_troop_first_name),
                (str_store_string,s1,":first_name"),
                (display_message,"@firstName:{s1}"),
                ## 名
                (troop_get_slot,":second_name",":troop",slot_troop_second_name),
                (str_store_string,s1,":second_name"),
                (display_message,"@secondName:{s1}"),
                ## 年龄
                (troop_get_slot,reg1,":troop",slot_troop_age),
                (display_message,"@age:{reg1}"),
                ## 性别
                (troop_get_type,reg1,":troop"),
                (display_message,"@sex:{reg1?str_man:str_woman}"),
                ## 财富
                (troop_get_slot,reg1,":troop",slot_troop_wealth),
                (display_message,"@wealth:{reg1}"),
                ## 被俘虏城市
                (troop_get_slot,":center",":troop",slot_troop_prisoner_of_party),
                (try_begin),
                    (gt,":center",0),
                    (str_store_party_name,s1,":center"),
                    (display_message,"@prisoner:{s1}"),
                (try_end),

                (display_message,"@-----------------------------------------------------"),

            ]),
            ("set_age_in_range",[
                (store_script_param,":troop",1),
                (store_script_param,":min_age",2),
                (store_script_param,":max_age",3),
                (store_random_in_range, ":age", ":min_age", ":max_age"),
                (call_script, "script_init_troop_age", ":troop", ":age"),
            ]),
            ("set_son_age",[
                (store_script_param,":father",1),
                (store_script_param,":son",2),
                (troop_get_slot,":father_age",":father",slot_troop_age),
                (store_random_in_range,":father_age_in_son_birth",20,30),
                (store_sub,":age",":father_age",":father_age_in_son_birth"),
                (call_script, "script_init_troop_age", ":son", ":age"),
            ]),
            ("troop_clear_items",[
                (store_script_param,":troop",1),
                (troop_get_inventory_capacity, ":inv_size", ":troop"),
                (try_for_range, ":i_slot", 0, ":inv_size"),
                    (troop_get_inventory_slot, ":item_id", ":troop", ":i_slot"),
                    (ge, ":item_id", 0),
                    (troop_remove_item,":troop",":item_id"),
                (try_end),
            ]),
            ("get_troop_all_items",[
                (store_script_param,":target_troop",1),
                (store_script_param,":source_troop",2),
                (call_script,"script_troop_clear_items",":target_troop"),

                (troop_get_inventory_capacity, ":inv_size", ":source_troop"),
                (try_for_range, ":i_slot", 0, ":inv_size"),
                    (troop_get_inventory_slot, ":item_id", ":source_troop", ":i_slot"),
                    (ge, ":item_id", 0),
                    (troop_add_item,":target_troop",":item_id"),
                (try_end),
            ]),
            ("get_troop_all_wealth",[
                (store_script_param,":target_troop",1),
                (store_script_param,":source_troop",2),
                (troop_get_slot,":wealth",":source_troop",slot_troop_wealth),
                (troop_get_slot,":renown",":source_troop",slot_troop_renown),
                (troop_get_slot,":father",":source_troop",slot_troop_father),
                (troop_get_slot,":mother",":source_troop",slot_troop_mother),
                (troop_get_slot,":spouse",":source_troop",slot_troop_spouse),
                (troop_get_slot,":guardian",":source_troop",slot_troop_guardian),
                (troop_get_slot,":betrothed",":source_troop",slot_troop_betrothed),

                (troop_set_slot,":target_troop",slot_troop_wealth,":wealth"),
                (troop_set_slot,":target_troop",slot_troop_renown,":renown"),
                (troop_set_slot,":target_troop",slot_troop_father,":father"),
                (troop_set_slot,":target_troop",slot_troop_mother,":mother"),
                (troop_set_slot,":target_troop",slot_troop_spouse,":spouse"),
                (troop_set_slot,":target_troop",slot_troop_guardian,":guardian"),
                (troop_set_slot,":target_troop",slot_troop_betrothed,":betrothed"),

                (store_faction_of_troop,":faction",":source_troop"),
                (try_begin),
                    (faction_slot_eq,":faction",slot_faction_leader,":source_troop"),
                    (faction_set_slot,":faction",slot_faction_leader,":target_troop"),
                (try_end),

                (call_script, "script_update_troop_notes",":target_troop"),
            ]),
            ("player_cosplay_anyone",[
                (store_script_param,":troop",1),

                (str_store_troop_name,s5,":troop"),
                (display_message,"@cosplay {s5}"),

                (troop_set_name,"trp_player",s5),
                (party_set_name,"p_main_party","str_s5_s_party"),

                (store_faction_of_troop,":faction",":troop"),
                (call_script,"script_player_join_faction",":faction"),

                (assign, "$player_has_homage", 1),

                (call_script,"script_get_center_of_lord",":troop","p_town_1"),
                (assign,":center",reg0),

                (call_script,"script_get_troop_all_items","trp_player",":troop"),

                (troop_equip_items,"trp_player"),
                (call_script,"script_get_troop_all_wealth","trp_player",":troop"),
                (call_script,"script_get_loard_all_centers","trp_player",":troop"),
                (troop_get_slot,":party",":troop",slot_troop_leaded_party),
                (call_script,"script_add_party_as_companions","p_main_party",":party",-1),
                (party_relocate_near_party,"p_main_party",":center",3),
                ## 设置被替换的人物为不启用
                (troop_set_slot,":troop",slot_troop_occupation,slto_inactive),
                (call_script,"script_update_all_notes"),
                ##(assign, "$current_startup_quest_phase", 4),
            ]),
            ## 获得领主的军事强度
            ("get_lord_strength",[
                (store_script_param_1,":leader"),
                (assign,":strength",0),
                (try_begin),
                    (ge,":leader"),
                    ## 战术加成
                    (store_skill_level,":tactics",skl_tactics,":leader"),
                    (store_mul,":tactics_strength",":tactics",2),
                    (val_add,":strength",":tactics_strength"),
                    ## 教练加成
                    (store_skill_level,":trainer",skl_trainer,":leader"),
                    (store_mul,":trainer_strength",":trainer",2),
                    (val_add,":strength",":trainer_strength"),
                    ## 性格加成
                    (this_or_next|troop_slot_eq,":leader",slot_lord_reputation_type,lrep_martial),
                    (troop_slot_eq,":leader",slot_lord_reputation_type,lrep_quarrelsome),
                    (val_add,":strength",3),
                    ## 性格缺陷
                    (troop_slot_eq,":leader",slot_lord_reputation_type,lrep_custodian),
                    (val_sub,":strength",3),
                (try_end),
                (assign,reg0,":strength"),
            ]),
            ## 更新领主财富
            ("update_lord_wealth",[
                 (store_script_param_1, ":lord_no"),
                 (store_script_param_2, ":value"),
                 ## 0:失去钱 1：获得钱
                 (store_script_param, ":type",3),

                 (troop_get_slot,":wealth",":lord_no",slot_troop_wealth),
                 (try_begin),
                     (gt,":type",0),
                     (val_add,":wealth",":value"),
                 (else_try),
                    (val_sub,":wealth",":value"),
                 (try_end),
                 (troop_set_slot,":lord_no",slot_troop_wealth,":wealth"),
             ]),
            ("get_troop_inventory_free_amount",
                [(store_script_param, ":troop_no", 1),
                 (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
                 (assign, ":count", 0),
                 ## 前边10个是人物的装备栏（有可能第0个不是，只有9个）
                 (try_for_range, ":i_slot", 10, ":inv_cap"),
                   (troop_get_inventory_slot, ":cur_item", ":troop_no", ":i_slot"),
                   (eq, ":cur_item", -1),
                   (val_add, ":count", 1),
                 (try_end),
                 (assign, reg0, ":count"),
            ]),
        ]),
        ("Append@strings",mergeList(
            parseFirstStrings(first),
            parseSecondStrings(second),
            [
                ("s5_leave_home","{s5} leave home"),
                ("s5_go_home","{s5} go home"),
                ("s1_s2_name","{s1} {s2}"),
            ],
        ))
    ],
    "internationals":{
        "cns":{
            "game_strings":mergeList(
                parseCnsFirstStrings(first),
                parseCnsSecondStrings(second),
                [
                    "str_s5_leave_home|{s5}出 门 了",
                    "str_s5_go_home|{s5}回 家 了",
                    "str_s1_s2_name|{s1}{s2}",
                ]
            ),
        }
    }
}