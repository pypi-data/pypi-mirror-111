from smart_module.module_system.module_game_menus import *
from smart_module.module_system.process_operations import *


def save_game_menu_item(ofile,variable_list,variable_uses,menu_item,tag_uses,quick_strings):
  ofile.write(" mno_%s "%(menu_item[0]))
  save_statement_block(ofile,0, 1, menu_item[1], variable_list, variable_uses,tag_uses,quick_strings)
  ofile.write(" %s "%(menu_item[2].replace(" ","_")))
  save_statement_block(ofile,0, 1, menu_item[3], variable_list, variable_uses,tag_uses,quick_strings)
  door_name = "."
  if (len(menu_item) > 4):
    door_name = menu_item[4]
  ofile.write(" %s "%(door_name.replace(" ","_")))
    

def save_game_menus(variable_list,variable_uses,tag_uses,quick_strings,export_dir):
  ofile = open(export_dir + "menus.txt","w",encoding="utf-8")
  ofile.write("menusfile version 1\n")
  ofile.write(" %d\n"%(len(game_menus)))
  for game_menu in game_menus:
    ofile.write("menu_%s %d %s %s"%(game_menu[0],game_menu[1],game_menu[2].replace(" ","_"),game_menu[3]))
    save_statement_block(ofile,0,1, game_menu[4]  , variable_list, variable_uses,tag_uses,quick_strings)
    menu_items = game_menu[5]
    ofile.write("%d\n"%(len(menu_items)))
    for menu_item in menu_items:
      save_game_menu_item(ofile,variable_list,variable_uses,menu_item,tag_uses,quick_strings)
    ofile.write("\n")
  ofile.close()

def save_python_header(src_dir):
  ofile = open(src_dir + "ID_menus.py","w",encoding="utf-8")
  for i_game_menu in range(len(game_menus)):
    ofile.write("menu_%s = %d\n"%(game_menus[i_game_menu][0],i_game_menu))
  ofile.close()


def processGameMenus(context):
  print( "Exporting game menus data...")

  configParser = context.configParser
  src_dir = configParser.getSrcDir()
  export_dir = configParser.getExportDir()

  save_python_header(src_dir)
  variable_uses = []
  variables = load_variables(export_dir, variable_uses)
  tag_uses = load_tag_uses(export_dir)
  quick_strings = load_quick_strings(export_dir)
  save_game_menus(variables, variable_uses, tag_uses, quick_strings,export_dir)
  save_variables(export_dir, variables, variable_uses)
  save_tag_uses(export_dir, tag_uses)
  save_quick_strings(export_dir, quick_strings)