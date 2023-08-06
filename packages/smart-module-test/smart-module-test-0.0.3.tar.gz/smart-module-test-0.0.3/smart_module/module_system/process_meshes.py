from smart_module.module_system.module_info import *
from smart_module.module_system.module_meshes import *

from smart_module.module_system.process_common import *



def save_meshes(export_dir):
  ofile = open(export_dir + "meshes.txt","w",encoding="utf-8")
  ofile.write("%d\n"%len(meshes))
  for i_mesh in range(len(meshes)):
    mesh = meshes[i_mesh]
    ofile.write("mesh_%s %d %s %f %f %f %f %f %f %f %f %f\n"%(mesh[0],mesh[1],replace_spaces(mesh[2]),mesh[3],mesh[4],mesh[5],mesh[6],mesh[7],mesh[8],mesh[9],mesh[10],mesh[11]))
  ofile.close()

def save_python_header(src_dir):
  ofile = open(src_dir + "ID_meshes.py","w",encoding="utf-8")
  for i_mesh in range(len(meshes)):
    ofile.write("mesh_%s = %d\n"%(meshes[i_mesh][0],i_mesh))
  ofile.write("\n\n")
  ofile.close()


def processMeshs(context):
  print( "Exporting meshes...")

  configParser = context.configParser
  src_dir = configParser.getSrcDir()
  export_dir = configParser.getExportDir()

  save_python_header(src_dir)
  save_meshes(export_dir)
