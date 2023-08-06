from smart_module.module_system.ID_troops import *
from smart_module.module_system.header_dialogs import *
from smart_module.module_system.header_game_menus import *
from smart_module.module_system.module_mission_templates import *

testMode = {
    "name":"testMode",
    "enable":True,
    "version": "v2.0.0",
    "desc":"与测试相关的功能，各种常用场景，进入大地图，进入村庄，进入战场等等",
    "actions":[
        ("GameStartMenu",[
            ("test_map",[],"TEST 【map】",
             [
                 (call_script,"script_go_to_center",-1,-1,100000,5000,1,1,1),
            ]),
            ("test_village",[],"TEST 【village】",
             [
                 (call_script,"script_go_to_center","p_village_1",-1,100000,5000,1,-1,-1),
                 (call_script,"script_init_village_base_basic_business_data"),
            ]),
            ("test_alley",[],"TEST 【alley】",
             [
                 (call_script,"script_create_battle_for_player","p_town_1",slot_town_alley,20,20),
             ]),

             ("test_arena",[],"TEST 【arena】",
             [
                 (call_script,"script_create_battle_for_player","p_town_1",slot_town_arena,20,20),
             ]),

            ("test_tavern",[],"TEST 【tavern】",
             [
                 (call_script,"script_create_battle_for_player","p_town_1",slot_town_tavern,20,20),
             ]),

            ("test_prison",[],"TEST 【prison】",
             [
                 (call_script,"script_create_battle_for_player","p_town_1",slot_town_prison,20,20),
             ]),
            ("test_castle",[],"TEST 【castle】",
             [
                 (call_script,"script_create_battle_for_player","p_town_1",slot_town_castle,20,20),
             ]),

            ("test_center",[],"TEST 【center】",
             [
                 (call_script,"script_create_battle_for_player","p_town_1",slot_town_center,20,20),
             ]),

            ("test_plain",[],"TEST 【plain】",
             [
                 (call_script,"script_create_battle_for_player","scn_random_scene_plain",-1,20,20),
            ]),

            ("test_zendar",[],"TEST 【zendar】",
             [
                (set_visitor, 0, "trp_player"),
                (set_jump_mission, "mt_town_center"),
                (jump_to_scene, "scn_zendar_center"),


                (troop_set_name,"trp_player","@test"),
                (party_set_name,"p_main_party","@test"),
                (troop_add_item, "trp_player", "itm_saddle_horse", 0),
                (troop_add_item, "trp_player", "itm_courser", 0),
                (troop_add_item, "trp_player", "itm_courtly_outfit", 0),
                (troop_add_item, "trp_player", "itm_heraldic_mail_with_tabard", 0),
                (troop_add_item, "trp_player", "itm_red_gambeson", 0),
                (troop_add_item, "trp_player", "itm_sword_medieval_c", 0),
                (troop_add_item, "trp_player", "itm_tab_shield_kite_cav_b", 0),
                (troop_add_item, "trp_player", "itm_light_lance", 0),

                 (troop_raise_skill,"trp_player",skl_riding,10),
                 (troop_raise_skill,"trp_player",skl_leadership,10),

                (troop_raise_attribute,"trp_player",sf_base_att_str,10),
                (troop_raise_attribute,"trp_player",sf_base_att_agi,10),
                (troop_raise_attribute,"trp_player",sf_base_att_int,10),
                (troop_raise_attribute,"trp_player",sf_base_att_cha,10),

                (troop_add_items,"trp_player","itm_dried_meat",10),
                 # (try_for_range,":npc","trp_npc1","trp_npc16"),
                 #    (call_script,"script_recruit_troop_as_companion",":npc"),
                 #    (troop_raise_skill,":npc",skl_persuasion,1),
                 # (try_end),

                 (party_add_members,"p_main_party","trp_swadian_knight",70),
                 (troop_add_gold,"trp_player",100000),
                (troop_set_slot,"trp_player",slot_troop_renown,5000),

                (troop_raise_skill,"trp_player",skl_prisoner_management,10),
                (party_add_prisoners, "p_main_party", "trp_swadian_knight", 10),



                (change_screen_mission),
            ]),
        ]),
        ("Prepend@dialogs|start&1:Surrender_or_die%^&3:battle_reason_stated&4",[
            [trp_constable_hareck, "start", [], "what can I do for you?", "constable_hareck_hi",[]],

            [anyone | plyr, "constable_hareck_hi", [], "I want to be a king.", "constable_hareck_to_be_king", []],
            ## 选择国王
            [anyone, "constable_hareck_to_be_king", [], "who you want to be?", "constable_hareck_to_be_king_choice_king", []],
            [anyone | plyr | repeat_for_troops, "constable_hareck_to_be_king_choice_king", [
                (store_repeat_object,":king"),
                (is_between,":king",kings_begin,kings_end),
                (store_faction_of_troop,":faction",":king"),
                (str_store_faction_name,s1,":faction"),
                (str_store_troop_name,s2,":king"),
            ], "{s1} {s2}", "constable_hareck_to_be_king_choice_king_end", [
                (store_repeat_object,":king"),
                (assign,reg1,":king"),
            ]],
            [anyone, "constable_hareck_to_be_king_choice_king_end", [
                (assign,":king",reg1),
                (store_faction_of_troop,":faction",":king"),
                (str_store_faction_name,s1,":faction"),
                (str_store_troop_name,s2,":king"),
            ], "now,you are the king {s2} of faction {s1}.", "close_window", [
                (assign,":king",reg1),
                (call_script,"script_player_cosplay_anyone",":king"),
                (change_screen_map),
            ]],


            [anyone | plyr, "constable_hareck_hi", [], "I want to be a lord.", "constable_hareck_to_be_lord", []],
            ## 选择阵营
            [anyone, "constable_hareck_to_be_lord", [], "which faction you want to be lord?", "constable_hareck_to_be_lord_choice_faction", []],
            [anyone | plyr | repeat_for_factions, "constable_hareck_to_be_lord_choice_faction", [
                (store_repeat_object,":faction"),
                (is_between,":faction",npc_kingdoms_begin,npc_kingdoms_end),
                (str_store_faction_name,s1,":faction"),
            ], "{s1}", "constable_hareck_to_be_lord_choice_faction_end", [
                (store_repeat_object,":faction"),
                (assign,reg1,":faction"),
            ]],
            ## 选择领主
            [anyone, "constable_hareck_to_be_lord_choice_faction_end", [], "who you want to be?", "constable_hareck_to_be_lord_choice_lord", []],
            [anyone | plyr | repeat_for_troops, "constable_hareck_to_be_lord_choice_lord", [
                (store_repeat_object,":lord"),
                (is_between,":lord",lords_begin,lords_end),
                (store_faction_of_troop,":faction",":lord"),
                (eq,":faction",reg1),
                (str_store_troop_name,s1,":lord"),
            ], "{s1}", "constable_hareck_to_be_lord_choice_lord_end", [
                (store_repeat_object,":lord"),
                (assign,reg2,":lord"),
            ]],
            [anyone, "constable_hareck_to_be_lord_choice_lord_end", [
                (assign,":faction",reg1),
                (assign,":lord",reg2),
                (str_store_faction_name,s1,":faction"),
                (str_store_troop_name,s2,":lord"),
            ], "now,you are the {s2} lord of {s1} faction", "close_window", [
                (assign,":lord",reg2),
                (call_script,"script_player_cosplay_anyone",":lord"),
                (change_screen_map),
            ]],

            [anyone | plyr, "constable_hareck_hi", [], "never mind!", "close_window", []],
        ])
    ],
    "internationals":{
        "cns":{
            "game_menus":[
                "mno_test_alley|测 试 【 街 道 】",
                "mno_test_map|测 试 【 大 地 图 】",
                "mno_test_village|测 试 【 村 庄 】",
                "mno_test_arena|测 试 【 竞 技 场 】",
                "mno_test_tavern|测 试 【 酒 馆 】",
                "mno_test_prison|测 试 【 监 狱 】",
                "mno_test_castle|测 试 【 大 厅 】",
                "mno_test_center|测 试 【 地 形 】",
                "mno_test_zendar|测 试 【 禅 达 】",
            ],
            "dialogs":[
                "dlga_start:constable_hareck_hi|有 什 么 可 以 帮 助 你 的？",
                "dlga_constable_hareck_hi:constable_hareck_to_be_king|我 想 做 国 王",
                "dlga_constable_hareck_to_be_king:constable_hareck_to_be_king_choice_king|你 想 成 为 哪 个 国 王？",
                "dlga_constable_hareck_to_be_king_choice_king_end:close_window|现 在, 你 已 经 是 {s1} 的 {s2} 国 王 了!",
                "dlga_constable_hareck_hi:constable_hareck_to_be_lord|我 想 做 领 主",
                "dlga_constable_hareck_to_be_lord:constable_hareck_to_be_lord_choice_faction|你 想 成 为 哪 个 国 家 的 领 主?",
                "dlga_constable_hareck_to_be_lord_choice_faction_end:constable_hareck_to_be_lord_choice_lord|你 想 成 为 这 个 国 家 的 哪 位 领 主?",
                "dlga_constable_hareck_to_be_lord_choice_lord_end:close_window|现 在, 你 已 经 是 {s1} 的 {s2} 领 主 了!",

                "dlga_constable_hareck_hi:close_window|不 需 要",
            ]
        }
    },
}