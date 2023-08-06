from smart_module.module_system.module_presentations import presentations
from smart_module.module_system.process_operations import *


def save_presentations(variable_list,variable_uses,tag_uses,quick_strings,export_dir):
  ofile = open(export_dir + "presentations.txt","w",encoding="utf-8")
  ofile.write("presentationsfile version 1\n")
  ofile.write(" %d\n"%(len(presentations)))
  for presentation in presentations:
    ofile.write("prsnt_%s %d %d "%(presentation[0], presentation[1], presentation[2]))
    save_simple_triggers(ofile,presentation[3], variable_list,variable_uses,tag_uses,quick_strings)
    ofile.write("\n")
  ofile.close()


def save_python_header(src_dir):
  file = open(src_dir + "ID_presentations.py","w",encoding="utf-8")
  for i_presentation in range(len(presentations)):
    file.write("prsnt_%s = %d\n"%(presentations[i_presentation][0],i_presentation))
  file.close()


def processPresentations(context):
  print( "Exporting presentations...")

  configParser = context.configParser
  src_dir = configParser.getSrcDir()
  export_dir = configParser.getExportDir()

  save_python_header(src_dir)
  variable_uses = []
  variables = load_variables(export_dir,variable_uses)
  tag_uses = load_tag_uses(export_dir)
  quick_strings = load_quick_strings(export_dir)
  save_presentations(variables,variable_uses,tag_uses,quick_strings,export_dir)
  save_variables(export_dir,variables,variable_uses)
  save_tag_uses(export_dir,tag_uses)
  save_quick_strings(export_dir,quick_strings)
