
from smart_module.module_system.module_dialogs import *
from smart_module.module_system.module_game_menus import game_menus
from smart_module.module_system.module_info import *
from smart_module.module_system.module_mission_templates import mission_templates
from smart_module.module_system.module_presentations import *
from smart_module.module_system.module_scene_props import scene_props
from smart_module.module_system.module_scripts import scripts
from smart_module.module_system.module_simple_triggers import *
from smart_module.module_system.module_triggers import *
from smart_module.module_system.module_variables import reserved_variables
from smart_module.module_system.process_operations import *

def compile_all_global_vars(variable_list,variable_uses, triggers, sentences, game_menus, mission_templates, scripts, simple_triggers):
  temp_list = []
  list_type = type(temp_list)
  for varb in reserved_variables:
    try:
      add_variable(varb, variable_list, variable_uses)
    except:
      print( "ERROR in variable:")
      ##print( variable)
  
  for trigger in triggers:
    try:
      compile_global_vars(trigger[3], variable_list,variable_uses),
      compile_global_vars(trigger[4], variable_list,variable_uses),
    except:
      print( "ERROR in trigger:")
      print( trigger)

  for scene_prop in scene_props:
    try:
      sp_triggers = scene_prop[4]
      for sp_trigger in sp_triggers:
        compile_global_vars(sp_trigger[1], variable_list,variable_uses)
    except:
      print( "ERROR in scene prop:")
      print( scene_prop)
      
  for sentence in sentences:
    try:
      compile_global_vars(sentence[2], variable_list,variable_uses),
      compile_global_vars(sentence[5], variable_list,variable_uses),
    except:
      print( "ERROR in dialog line:")
      print( sentence)

  for game_menu in game_menus:
    try:
      compile_global_vars(game_menu[4], variable_list,variable_uses)
      menu_items = game_menu[5]
      for menu_item in menu_items:
        compile_global_vars(menu_item[1], variable_list,variable_uses)
        compile_global_vars(menu_item[3], variable_list,variable_uses)
    except:
      print( "ERROR in game menu:")
      print( game_menu)

  for mission_template in mission_templates:
    try:
      mt_triggers = mission_template[5]
      for mt_trigger in mt_triggers:
        compile_global_vars(mt_trigger[3], variable_list,variable_uses)
        compile_global_vars(mt_trigger[4], variable_list,variable_uses)
    except:
      print( "ERROR in mission template:")
      print( mission_template)

  for presentation in presentations:
    try:
      prsnt_triggers = presentation[3]
      for prsnt_trigger in prsnt_triggers:
        compile_global_vars(prsnt_trigger[1], variable_list,variable_uses)
    except RuntimeError as ex:
      print( "ERROR in presentation:")
      print( presentation)

  for i_script in range(len(scripts)):
    try:
      func = scripts[i_script]
      if (type(func[1]) == list_type):
        compile_global_vars(func[1], variable_list,variable_uses)
      else:
        compile_global_vars(func[2], variable_list,variable_uses)
    except RuntimeError as ex:
      print( "ERROR in script:")
      print( func)

  for simple_trigger in simple_triggers:
    try:
      compile_global_vars(simple_trigger[1]  , variable_list,variable_uses)
    except:
      print( "ERROR in simple trigger:")
      print( simple_trigger)



def processGlobalVariables(context):
  print( "Compiling all global variables...")

  configParser = context.configParser
  src_dir = configParser.getSrcDir()
  export_dir = configParser.getExportDir()

  variable_uses = []
  variables = load_variables(export_dir, variable_uses)


  compile_all_global_vars(variables, variable_uses,triggers, dialogs, game_menus, mission_templates, scripts, simple_triggers)
  save_variables(export_dir, variables,variable_uses)
