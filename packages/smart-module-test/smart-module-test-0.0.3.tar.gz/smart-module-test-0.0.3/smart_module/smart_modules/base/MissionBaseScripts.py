## 用于编写一些ai方面的功能
from smart_module.module_system.header_operations import *
from smart_module.module_system.header_skills import *
from smart_module.module_system.module_constants import *

missionBaseScripts={
    "name":"AiBaseScripts",
    "enable":True,
    "version": "v2.0.0",
    "desc":"与场景或战场相关的操作",
    "actions":[
        ("Append@scripts",[
            ("create_battle_for_player", [
                (store_script_param_1, ":center"),
                (store_script_param_2, ":place"),
                (store_script_param, ":companies_nums", 3),
                (store_script_param, ":enemies_nums", 4),

                # (party_get_slot, ":scene_no", "p_town_1", slot_town_alley),
                (try_begin),
                (gt, ":place", 0),
                (party_get_slot, ":scene_no", ":center", ":place"),
                (else_try),
                (assign, ":scene_no", ":center"),
                (try_end),

                (modify_visitors_at_site, ":scene_no"),

                (reset_visitors),
                (set_visitor, 0, "trp_player"),

                (party_add_members, "p_main_party", "trp_swadian_knight", ":companies_nums"),

                (troop_add_item, "trp_player", "itm_saddle_horse", 0),
                (troop_add_item, "trp_player", "itm_courser", 0),
                (troop_add_item, "trp_player", "itm_courtly_outfit", 0),
                (troop_add_item, "trp_player", "itm_heraldic_mail_with_tabard", 0),
                (troop_add_item, "trp_player", "itm_red_gambeson", 0),
                (troop_add_item, "trp_player", "itm_sword_medieval_c", 0),
                (troop_add_item, "trp_player", "itm_tab_shield_kite_cav_b", 0),
                (troop_add_item, "trp_player", "itm_light_lance", 0),
                (troop_raise_skill, "trp_player", skl_riding, 10),
                (troop_equip_items, "trp_player"),

                (val_mul, ":enemies_nums", 3),
                (set_visitors, 2, "trp_bandit", ":enemies_nums"),

                (set_jump_mission, "mt_alley_fight"),
                (jump_to_scene, ":scene_no"),
                (change_screen_mission),
            ]),
            ("go_to_center", [
                ## 地点  -1代表大地图
                (store_script_param_1, ":center"),
                ## 地区 酒馆，街道等等  -1代表 村庄中心（村庄只有一个地区）
                (store_script_param_2, ":place"),
                (store_script_param, ":gold_amonut", 3),
                (store_script_param, ":renown_amonut", 4),
                (store_script_param, ":has_companion", 5),
                (store_script_param, ":has_soldier", 6),
                (store_script_param, ":has_prisoner", 7),

                ## 名称
                (troop_set_name, "trp_player", "@test"),
                (party_set_name, "p_main_party", "@test"),
                ## 基础物品
                (troop_add_item, "trp_player", "itm_saddle_horse", 0),
                (troop_add_item, "trp_player", "itm_courser", 0),
                (troop_add_item, "trp_player", "itm_courtly_outfit", 0),
                (troop_add_item, "trp_player", "itm_heraldic_mail_with_tabard", 0),
                (troop_add_item, "trp_player", "itm_red_gambeson", 0),
                (troop_add_item, "trp_player", "itm_sword_medieval_c", 0),
                (troop_add_item, "trp_player", "itm_tab_shield_kite_cav_b", 0),
                (troop_add_item, "trp_player", "itm_light_lance", 0),
                (troop_add_items, "trp_player", "itm_dried_meat", 10),
                ## 穿上装备
                (troop_equip_items, "trp_player"),

                ## 基础技能
                (troop_raise_skill, "trp_player", skl_riding, 10),
                (troop_raise_skill, "trp_player", skl_leadership, 10),
                (troop_raise_attribute, "trp_player", sf_base_att_str, 10),
                (troop_raise_attribute, "trp_player", sf_base_att_agi, 100),
                (troop_raise_attribute, "trp_player", sf_base_att_int, 10),
                (troop_raise_attribute, "trp_player", sf_base_att_cha, 10),

                ## 金币
                (troop_add_gold, "trp_player", ":gold_amonut"),
                ## 声望
                (troop_set_slot, "trp_player", slot_troop_renown, ":renown_amonut"),
                ## 士兵
                (try_begin),
                (gt, ":has_soldier", 0),
                (party_add_members, "p_main_party", "trp_swadian_knight", 70),
                (try_end),
                ## 同伴
                (try_begin),
                (gt, ":has_companion", 0),
                (try_for_range, ":npc", companions_begin, companions_end),
                (call_script, "script_recruit_troop_as_companion", ":npc"),
                (troop_raise_skill, ":npc", skl_persuasion, 1),
                (try_end),
                (try_end),
                ## 奴隶
                (try_begin),
                (gt, ":has_prisoner", 0),
                (troop_raise_skill, "trp_player", skl_prisoner_management, 10),
                (party_add_prisoners, "p_main_party", "trp_swadian_knight", 10),
                (try_end),

                (try_begin),
                (eq, ":center", -1),
                (party_relocate_near_party, "p_main_party", "p_village_1", 3),
                (change_screen_map),
                (else_try),
                (assign, "$current_town", ":center"),
                (try_begin),
                (eq, ":scene_no", -1),
                (party_get_slot, ":scene_no", ":center", slot_castle_exterior),
                (set_jump_mission, "mt_village_center"),
                (jump_to_scene, ":scene_no"),
                (else_try),
                (party_get_slot, ":scene_no", ":center", ":place"),
                (set_jump_mission, "mt_town_center"),
                (jump_to_scene, ":scene_no"),
                (try_end),
                ## 更新访问者
                (modify_visitors_at_site, ":scene_no"),
                (reset_visitors),
                ## 设置村长
                (party_get_slot, ":village_elder_troop", ":center", slot_town_elder),
                (set_visitor, 11, ":village_elder_troop"),
                ## 初始化村民
                (call_script, "script_init_town_walkers"),
                (change_screen_mission),
                (try_end),
            ]),
        ])
    ],
}