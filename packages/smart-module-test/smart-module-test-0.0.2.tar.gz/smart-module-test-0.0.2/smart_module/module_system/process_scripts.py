from smart_module.module_system.process_operations import *


def save_scripts(variable_list,variable_uses,scripts,tag_uses,quick_strings,export_dir):
  file = open(export_dir + "scripts.txt","w",encoding="utf-8")
  file.write("scriptsfile version 1\n")
  file.write("%d\n"%len(scripts))
  temp_list = []
  list_type = type(temp_list)
  for i_script in range(len(scripts)):
    func = scripts[i_script]
    if (type(func[1]) == list_type):
      file.write("%s -1\n"%(convert_to_identifier(func[0])))
      save_statement_block(file,convert_to_identifier(func[0]), 0,func[1], variable_list,variable_uses,tag_uses,quick_strings)
    else:
      file.write("%s %f\n"%(convert_to_identifier(func[0]), func[1]))
      save_statement_block(file,convert_to_identifier(func[0]), 0,func[2], variable_list,variable_uses,tag_uses,quick_strings)
    file.write("\n")
  file.close()

def save_python_header(src_dir):
  file = open(src_dir + "ID_scripts.py","w",encoding="utf-8")
  for i_script in range(len(scripts)):
    file.write("script_%s = %d\n"%(convert_to_identifier(scripts[i_script][0]),i_script))
  file.write("\n\n")
  file.close()


def processScripts(context):
  print("Exporting scripts...")

  configParser = context.configParser
  src_dir = configParser.getSrcDir()
  export_dir = configParser.getExportDir()

  save_python_header(src_dir)
  variable_uses = []
  variables = load_variables(export_dir, variable_uses)
  tag_uses = load_tag_uses(export_dir)
  quick_strings = load_quick_strings(export_dir)
  save_scripts(variables, variable_uses, scripts, tag_uses, quick_strings,export_dir)
  save_variables(export_dir, variables, variable_uses)
  save_tag_uses(export_dir, tag_uses)
  save_quick_strings(export_dir, quick_strings)
