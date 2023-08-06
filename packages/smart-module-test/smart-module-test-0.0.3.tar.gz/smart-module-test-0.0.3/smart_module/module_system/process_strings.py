import os.path

from smart_module.module_system.module_info import *
from smart_module.module_system.module_strings import *

from smart_module.module_system.process_common import *


def save_strings(strings,export_dir):
  ofile = open(export_dir + "strings.txt","w",encoding="utf-8")
  ofile.write("stringsfile version 1\n")
  ofile.write("%d\n"%len(strings))
  for i_string in range(len(strings)):
    str = strings[i_string]
    ofile.write("str_%s %s\n"%(convert_to_identifier(str[0]),replace_spaces(str[1])))
  ofile.close()

def save_python_header(src_dir):
  ##print(os.path.abspath(src_dir + "ID_strings.py"))
  ofile = open(src_dir + "ID_strings.py","w",encoding="utf-8")
  for i_string in range(len(strings)):
    ofile.write("str_%s = %d\n"%(convert_to_identifier(strings[i_string][0]),i_string))
  ofile.write("\n\n")
  ofile.close()


def processStrings(context):
  print( "Exporting strings...")

  configParser = context.configParser
  src_dir = configParser.getSrcDir()
  export_dir = configParser.getExportDir()

  save_python_header(src_dir)
  save_strings(strings,export_dir)

