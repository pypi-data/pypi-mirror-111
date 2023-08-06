from smart_module.module_system.module_info import *
from smart_module.module_system.module_info_pages import *

def save_info_pages(export_dir):
  ofile = open(export_dir + "info_pages.txt","w",encoding="utf-8")
  ofile.write("infopagesfile version 1\n")
  ofile.write("%d\n"%(len(info_pages)))
  for i_info_page in range(len(info_pages)):
    info_page = info_pages[i_info_page]
    ofile.write("ip_%s %s %s"%(info_page[0],info_page[1].replace(" ","_"), info_page[2].replace(" ","_")))
    ofile.write("ip_%s %s %s"%(info_page[0],info_page[1].replace(" ","_"), info_page[2].replace(" ","_")))
    ofile.write("\n")
  ofile.close()

def save_python_header(src_dir):
  ofile = open(src_dir + "ID_info_pages.py","w",encoding="utf-8")
  for i_info_page in range(len(info_pages)):
    ofile.write("ip_%s = %d\n"%(info_pages[i_info_page][0],i_info_page))
  ofile.write("\n\n")
  ofile.close()


def processInfoPages(context):
  print( "Exporting info_page data...")

  configParser = context.configParser
  src_dir = configParser.getSrcDir()
  export_dir = configParser.getExportDir()

  save_info_pages(export_dir)
  save_python_header(src_dir)
  
