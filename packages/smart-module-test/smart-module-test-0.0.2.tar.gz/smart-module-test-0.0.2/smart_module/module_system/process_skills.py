
from smart_module.module_system.module_skills import *
from smart_module.module_system.process_common import *

skill_name_pos = 1
skill_attribute_pos = 2
skill_max_level_pos= 3
skill_desc_pos = 4



def save_skills(export_dir):
  ofile = open(export_dir + "skills.txt","w",encoding="utf-8")
  ofile.write("%d\n"%(len(skills)))
  for i_skill in range(len(skills)):
    skill = skills[i_skill]
    ofile.write("skl_%s %s "%(skill[0], replace_spaces(skill[1])))
    ofile.write("%d %d %s\n"%(skill[skill_attribute_pos],skill[skill_max_level_pos],skill[skill_desc_pos].replace(" ","_")))
  ofile.close()

def save_python_header(src_dir):
  ofile = open(src_dir + "ID_skills.py","w",encoding="utf-8")
  for i_skill in range(len(skills)):
    ofile.write("skl_%s = %d\n"%(skills[i_skill][0],i_skill))
  ofile.write("\n\n")
  ofile.close()


def processSkills(context):
  print( "Exporting skills...")
  configParser = context.configParser
  src_dir = configParser.getSrcDir()
  export_dir = configParser.getExportDir()
  save_python_header(src_dir)
  save_skills(export_dir)
