from smart_module.module_system.module_tableau_materials import tableaus
from smart_module.module_system.process_operations import *


def save_tableau_materials(variable_list,variable_uses,tag_uses,quick_strings,export_dir):
  ofile = open(export_dir + "tableau_materials.txt","w",encoding="utf-8")
  ofile.write("%d\n"%(len(tableaus)))
  for tableau in tableaus:
    ofile.write("tab_%s %d %s %d %d %d %d %d %d"%(tableau[0], tableau[1], tableau[2], tableau[3], tableau[4], tableau[5], tableau[6], tableau[7], tableau[8]))
    save_statement_block(ofile, 0, 1, tableau[9], variable_list, variable_uses, tag_uses, quick_strings)
    ofile.write("\n")
  ofile.close()

def save_python_header(src_dir):
  ofile = open(src_dir + "ID_tableau_materials.py","w",encoding="utf-8")
  for i_tableau in range(len(tableaus)):
    ofile.write("tableau_%s = %d\n"%(tableaus[i_tableau][0],i_tableau))
  ofile.close()


def processTableauMaterials(context):
  print( "Exporting tableau materials data...")

  configParser = context.configParser
  src_dir = configParser.getSrcDir()
  export_dir = configParser.getExportDir()

  save_python_header(src_dir)
  variable_uses = []
  variables = load_variables(export_dir, variable_uses)
  tag_uses = load_tag_uses(export_dir)
  quick_strings = load_quick_strings(export_dir)
  save_tableau_materials(variables,variable_uses,tag_uses,quick_strings,export_dir)
  save_variables(export_dir,variables,variable_uses)
  save_tag_uses(export_dir, tag_uses)
  save_quick_strings(export_dir,quick_strings)
