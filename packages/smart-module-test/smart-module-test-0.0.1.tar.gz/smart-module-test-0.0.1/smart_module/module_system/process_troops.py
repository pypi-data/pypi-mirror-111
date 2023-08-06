
from smart_module.module_system.module_troops import *

from smart_module.module_system.process_common import *
#from process_operations import *

num_face_numeric_keys = 4

def save_troops(export_dir):
  file = open(export_dir + "troops.txt","w",encoding="utf-8")
  file.write("troopsfile version 2\n")
  file.write("%d "%len(troops))
  for troop in troops:
    troop_len = len(troop)
    if troop_len == 11:
      troop[11:11] = [0, 0, 0, 0, 0]
    elif troop_len == 12:
      troop[12:12] = [0, 0, 0, 0]
    elif troop_len == 13:
      troop[13:13] = [0, 0, 0]
    elif troop_len == 14:
      troop[14:14] = [0, 0]
    elif troop_len == 15:
      troop[15:15] = [0]
    if (troop[4] > 0):
#      add_tag_use(tag_uses,tag_scene,troop[4] & tsf_site_id_mask)
      id_no = find_object("trp",convert_to_identifier(troop[0]))
#      if (id_no >= 0):  add_tag_use(tag_uses,tag_troop,id_no)
#    if (troop[6] > 0):  add_tag_use(tag_uses,tag_faction,troop[6])

    file.write("\ntrp_%s %s %s %s %d %d %d %d %d %d\n  "%(convert_to_identifier(troop[0]),replace_spaces(troop[1]),replace_spaces(troop[2]), replace_spaces(str(troop[13])), troop[3],troop[4],troop[5], troop[6], troop[14], troop[15]))
    inventory_list = troop[7]
#    inventory_list.append(itm_arrows)
#    inventory_list.append(itm_bolts)
    for inventory_item in inventory_list:
#      add_tag_use(tag_uses,tag_item,inventory_item)
      file.write("%d 0 "%inventory_item)
    for i in range(64 - len(inventory_list)):
      file.write("-1 0 ")
    file.write("\n ")
    attrib = troop[8]
    strength = (attrib & 0xff)
    agility  = ((attrib >> 8)& 0xff)
    intelligence = ((attrib >> 16)& 0xff)
    charisma = ((attrib >> 24)& 0xff)
    starting_level = (attrib >> level_bits) & level_mask
#    gold = two_to_pow(2 + (attrib >> 12)& 0x0f) * random
    
    file.write(" %d %d %d %d %d\n"%(strength,agility,intelligence,charisma,starting_level))
    wp_word = troop[9]
    for wp in range(num_weapon_proficiencies):
      wp_level = wp_word & 0x3FF
      file.write(" %d"%wp_level)
      wp_word = wp_word >> 10
    file.write("\n")
      
    skill_array = troop[10]
    for i in range(num_skill_words):
      file.write("%d "%((skill_array >> (i * 32)) & 0xffffffff))
    file.write("\n  ")

    face_keys = [troop[11],troop[12]]
    
    for fckey in (face_keys):
      word_keys = []
      for word_no in range(num_face_numeric_keys):
        word_keys.append((fckey >> (64 * word_no)) & 0xFFFFFFFFFFFFFFFF)
      for word_no in range(num_face_numeric_keys):
        file.write("%d "%(word_keys[(num_face_numeric_keys -1) - word_no]))

    file.write("\n")
      
        

 #     word2 = (fckey >> 64) & 0xFFFFFFFFFFFFFFFF
 #     word3 = (fckey >> 128) & 0xFFFFFFFFFFFFFFFF
 #     word4 = (fckey >> 192) & 0xFFFFFFFFFFFFFFFF
#      file.write("%d %d %d %d "%(word4, word3, word2, word1))

#    face_keys = troop[10]
#    for fckey in (face_keys):
#      file.write("%d "%(fckey))
#    for i in range(4 - len(face_keys)):
#      file.write("0 ")
      
    
  file.close()

def two_to_pow(x):
  result = 1
  for i in range(x):
    result = result * 2
  return result

def save_python_header(src_dir):
  file = open(src_dir + "ID_troops.py","w",encoding="utf-8")
  for i_troop in range(len(troops)):
    file.write("trp_%s = %d\n"%(convert_to_identifier(troops[i_troop][0]),i_troop))
  file.close()



def processTroops(context):
    print( "Exporting troops data")

    configParser = context.configParser
    src_dir = configParser.getSrcDir()
    export_dir = configParser.getExportDir()

    #tag_uses = load_tag_uses(export_dir)
    save_python_header(src_dir)
    save_troops(export_dir)
    #save_tag_uses(export_dir, tag_uses)
    #print( "Generating C header...")
    #save_c_header()
    #print( "Generating Python header...")
    #print( "Finished.")
