# -*- coding: utf-8 -*-
import os

from smart_module.module_system.process_operations import save_variables


def processInit(context):
  print(("Initializing..."))
  configParser = context.configParser
  export_dir = configParser.getExportDir()

  try:
    os.remove(export_dir + 'tag_uses.txt')
  except:
    a = []
  try:
    os.remove(export_dir + 'quick_strings.txt')
  except:
    a = []
  try:
    os.remove(export_dir + 'variables.txt')
  except:
    a = []
  try:
    os.remove(export_dir + 'variable_uses.txt')
  except:
    a = []

  variables = []
  variable_uses = []
  try:
    file = open("variables.txt","r",encoding="utf-8")
    var_list = file.readlines()
    file.close()
    for v in var_list:
      vv = v.strip()
      if vv:
        variables.append(vv)
        variable_uses.append(int(1))
    save_variables(export_dir, variables, variable_uses)
  except:
    print(("variables.txt not found. Creating new variables.txt file"))
