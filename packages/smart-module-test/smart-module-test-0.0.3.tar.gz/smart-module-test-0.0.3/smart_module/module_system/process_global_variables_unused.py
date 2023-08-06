from smart_module.module_system.module_info import *
from smart_module.module_system.process_common import *
from smart_module.module_system.process_operations import *


def processGlobalVariablesUnused(context):
  print( "Checking global variable usages...")

  configParser = context.configParser
  src_dir = configParser.getSrcDir()
  export_dir = configParser.getExportDir()

  variable_uses = []
  variables = load_variables(export_dir,variable_uses)
  i = 0
  while (i < len(variables)):
    if (variable_uses[i] == 0):
      print( "WARNING: Global variable never used: " + variables[i])
    i = i + 1
