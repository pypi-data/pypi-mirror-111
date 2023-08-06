
from smart_module.module_system.module_simple_triggers import simple_triggers
from smart_module.module_system.process_operations import *


def save_simple_triggers(variable_list,variable_uses,triggers,tag_uses,quick_strings,export_dir):
  file = open(export_dir + "simple_triggers.txt","w")
  file.write("simple_triggers_file version 1\n")
  file.write("%d\n"%len(simple_triggers))
  for i in range(len(simple_triggers)):
    simple_trigger = simple_triggers[i]
    file.write("%f "%(simple_trigger[0]))
    save_statement_block(file,0, 1, simple_trigger[1]  , variable_list,variable_uses,tag_uses,quick_strings)
    file.write("\n")
  file.close()



def processSimpleTriggers(context):
  print( "exporting simple triggers...")

  configParser = context.configParser
  src_dir = configParser.getSrcDir()
  export_dir = configParser.getExportDir()

  variable_uses = []
  variables = load_variables(export_dir, variable_uses)
  tag_uses = load_tag_uses(export_dir)
  quick_strings = load_quick_strings(export_dir)
  save_simple_triggers(variables, variable_uses, simple_triggers, tag_uses, quick_strings,export_dir)
  save_variables(export_dir, variables, variable_uses)
  save_tag_uses(export_dir, tag_uses)
  save_quick_strings(export_dir, quick_strings)
  # print "finished."
