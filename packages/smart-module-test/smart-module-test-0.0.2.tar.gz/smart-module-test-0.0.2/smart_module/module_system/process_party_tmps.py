
from smart_module.module_system.module_party_templates import *
#from process_operations import *

from smart_module.module_system.process_common import *

def save_party_template_troop(file,troop):
  if troop:
#    add_tag_use(tag_uses,tag_troop,troop[0])
    file.write("%d %d %d "%(troop[0],troop[1],troop[2]))
    if (len(troop) > 3):
      file.write("%d "%troop[3])
    else:
      file.write("0 ")
  else:
    file.write("-1 ")
    
def save_party_templates(export_dir):
  file = open(export_dir + "party_templates.txt","w",encoding="utf-8")
  file.write("partytemplatesfile version 1\n")
  file.write("%d\n"%(len(party_templates)))
  for party_template in party_templates:
#    add_tag_use(tag_uses,tag_faction,party_template[4])
    file.write("pt_%s %s %d %d %d %d "%(convert_to_identifier(party_template[0]),replace_spaces(party_template[1]),party_template[2],party_template[3], party_template[4], party_template[5]))
    members = party_template[6]
    if (len(members) > 6):
      print( "Error! NUMBER OF TEMPLATE MEMBERS EXCEEDS 6 " + party_template[0])
      members = members[0:6]
    for party_template_member in members:
      save_party_template_troop(file,party_template_member)
    for i in range(6 - len(members)):
      save_party_template_troop(file,0)
    file.write("\n")
  file.close()

def save_python_header(src_dir):
  file = open(src_dir + "ID_party_templates.py","w",encoding="utf-8")
  for i_party_template in range(len(party_templates)):
    file.write("pt_%s = %d\n"%(convert_to_identifier(party_templates[i_party_template][0]),i_party_template))
  file.close()


def processPartyTmps(context):
    print( "Exporting party_template data...")

    configParser = context.configParser
    src_dir = configParser.getSrcDir()
    export_dir = configParser.getExportDir()

    #tag_uses = load_tag_uses(export_dir)
    save_python_header(src_dir)
    save_party_templates(export_dir)
    #save_tag_uses(export_dir, tag_uses)
