from smart_module.module_system.module_info import *
from smart_module.module_system.module_music import *

def save_python_header(src_dir):
  ofile = open(src_dir + "ID_music.py","w",encoding="utf-8")
  for i_track in range(len(tracks)):
    ofile.write("track_%s = %d\n"%(tracks[i_track][0],i_track))
  ofile.write("\n\n")
  ofile.close()

def save_tracks(export_dir):
  file = open(export_dir + "music.txt","w",encoding="utf-8")
  file.write("%d\n"%len(tracks))
  for track in tracks:
    file.write("%s %d %d\n"%(track[1], track[2], (track[2] | track[3])))
  file.close()


def processMusic(context):
  print( "Exporting tracks...")

  configParser = context.configParser
  src_dir = configParser.getSrcDir()
  export_dir = configParser.getExportDir()

  save_python_header(src_dir)
  save_tracks(export_dir)
