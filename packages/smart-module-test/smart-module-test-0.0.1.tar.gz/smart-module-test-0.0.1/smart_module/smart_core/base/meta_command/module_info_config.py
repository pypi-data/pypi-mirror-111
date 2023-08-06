from smart_module.module_system.module_animations import animations
from smart_module.module_system.module_dialogs import dialogs
from smart_module.module_system.module_factions import factions
from smart_module.module_system.module_game_menus import game_menus
from smart_module.module_system.module_info_pages import info_pages
from smart_module.module_system.module_items import items
from smart_module.module_system.module_map_icons import map_icons
from smart_module.module_system.module_meshes import meshes
from smart_module.module_system.module_mission_templates import mission_templates
from smart_module.module_system.module_music import tracks
from smart_module.module_system.module_particle_systems import particle_systems
from smart_module.module_system.module_parties import parties
from smart_module.module_system.module_party_templates import party_templates
from smart_module.module_system.module_postfx import postfx_params
from smart_module.module_system.module_presentations import presentations
from smart_module.module_system.module_quests import quests
from smart_module.module_system.module_scene_props import scene_props
from smart_module.module_system.module_scenes import scenes
from smart_module.module_system.module_scripts import scripts
from smart_module.module_system.module_simple_triggers import simple_triggers
from smart_module.module_system.module_skills import skills
from smart_module.module_system.module_skins import skins
from smart_module.module_system.module_sounds import sounds
from smart_module.module_system.module_strings import strings
from smart_module.module_system.module_tableau_materials import tableaus
from smart_module.module_system.module_triggers import triggers
from smart_module.module_system.module_troops import troops

################################################
###
### 所有数据映射集合
### datas:数据集合
### level:数据优先级别（数值越小级别越高）
###
################################################

moduleDataMaping = {
    "factions":{
        "datas":factions,
        "level":0,
    },
    "troops":{
        "datas":troops,
        "level":0,
    },
    "skills":{
        "datas":skills,
        "level":0,
    },
    "skins":{
        "datas":skins,
        "level":0,
    },
    "items":{
        "datas":items,
        "level":0,
    },
    "parties":{
        "datas":parties,
        "level":0,
    },
    "party_templates":{
        "datas":party_templates,
        "level":2,
    },
    "scripts":{
        "datas":scripts,
        "level":5,
    },
    "triggers":{
        "datas":triggers,
        "level":10,
    },
    "simple_triggers":{
        "datas":simple_triggers,
        "level":10,
    },
    "dialogs":{
        "datas":dialogs,
        "level":10,
    },
    "game_menus":{
        "datas":game_menus,
        "level":10,
    },
    "mission_templates":{
        "datas":mission_templates,
        "level":2,
    },
    "quests":{
        "datas":quests,
        "level":0,
    },
    "strings":{
        "datas":strings,
        "level":0,
    },
    "presentations":{
        "datas":presentations,
        "level":10,
    },
    "map_icons":{
        "datas":map_icons,
        "level":0,
    },
    "particle_systems":{
        "datas":particle_systems,
        "level":0,
    },
    "scenes":{
        "datas":scenes,
        "level":0,
    },
    "info_pages":{
        "datas":info_pages,
        "level":0,
    },
    "tableaus":{
        "datas":tableaus,
        "level":5,
    },
    "meshes":{
        "datas":meshes,
        "level":0,
    },
    "postfx_params":{
        "datas":postfx_params,
        "level":0,
    },
    "scene_props":{
        "datas":scene_props,
        "level":5,
    },
    "tracks":{
        "datas":tracks,
        "level":0,
    },
    "sounds":{
        "datas":sounds,
        "level":0,
    },
    "animations":{
        "datas":animations,
        "level":0,
    },
}