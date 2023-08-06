
from smart_module.module_system.module_quests import *


def save_quests(export_dir):
  ofile = open(export_dir + "quests.txt","w",encoding="utf-8")
  ofile.write("questsfile version 1\n")
  ofile.write("%d\n"%(len(quests)))
  for i_quest in range(len(quests)):
    quest = quests[i_quest]
    ofile.write("qst_%s %s %d "%(quest[0],(quest[1].replace(" ","_")),quest[2]))
    ofile.write("%s "%(quest[3].replace(" ","_")))
    ofile.write("\n")
  ofile.close()

def save_python_header(src_dir):
  ofile = open(src_dir + "ID_quests.py","w",encoding="utf-8")
  for i_quest in range(len(quests)):
    ofile.write("qst_%s = %d\n"%(quests[i_quest][0],i_quest))
  for i_quest in range(len(quests)):
    ofile.write("qsttag_%s = %d\n"%(quests[i_quest][0],opmask_quest_index|i_quest))
  ofile.write("\n\n")
  ofile.close()


def processQuests(context):
  print( "Exporting quest data...")

  configParser = context.configParser
  src_dir = configParser.getSrcDir()
  export_dir = configParser.getExportDir()

  save_quests(export_dir)
  save_python_header(src_dir)
  
