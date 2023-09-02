from System import *
import Manager
import Item
import Shop
import Library
import Shard
import Equipment
import Enemy
import Room
import Sound
import Bloodless
import Utility

def init():
    global shard_type_to_hsv
    shard_type_to_hsv = {
        "Skill":       (  0,   0, 100),
        "Trigger":     (  0, 100, 100),
        "Effective":   (230, 100,  80),
        "Directional": (270, 100, 100),
        "Enchant":     ( 60, 100, 100),
        "Familia":     (120, 100,  80)
    }
    global material_to_offset
    material_to_offset = {
        "MI_N1001_Body": [
            0x110E,
            0x113B,
            0x1175,
            0x11D5,
            0x8BDD,
            0x8C0A,
            0x8C44,
            0x8CA4
        ],
        "MI_N1001_Crystal": [
            0x1CC9,
            0x1CF6,
            0x1D30,
            0x1D90,
            0x1DF6,
            0x1E23,
            0x1E5D,
            0x1EBD,
            0x1A0CE,
            0x1A0FB,
            0x1A135,
            0x1A195,
            0x1A1FB,
            0x1A228,
            0x1A262,
            0x1A2C2
        ],
        "MI_N1001_Eye1": [
            0x104A,
            0x1077,
            0x10B1,
            0x1111,
            0x86D1,
            0x86FE,
            0x8738,
            0x8798
        ],
        "MI_N1001_Eye2": [
            0x104A,
            0x1077,
            0x10B1,
            0x1111,
            0x86D2,
            0x86FF,
            0x8739,
            0x8799
        ],
        "MI_N1001_Face": [
            0x104A,
            0x1077,
            0x10B1,
            0x1111,
            0x85A1,
            0x85CE,
            0x8608,
            0x8668
        ],
        "MI_N1001_Hair": [
            0x104A,
            0x1077,
            0x10B1,
            0x1111,
            0x86D1,
            0x86FE,
            0x8738,
            0x8798
        ],
        "MI_N1001_Mouth": [
            0x104A,
            0x1077,
            0x10B1,
            0x1111,
            0x86D2,
            0x86FF,
            0x8739,
            0x8799
        ],
        "MI_N1001_tongue": [
            0x1ABD,
            0x1AEA,
            0x1B24,
            0x1B84,
            0x13A24,
            0x13A51,
            0x13A8B,
            0x13AEB
        ],
        "MI_N2012": [
            0x1AC2,
            0x1E48,
            0xAA36,
            0xADBC
        ],
        "MI_N2012_Sharded": [
            0x1AC2,
            0x1E48,
            0xAA36,
            0xADBC
        ],
        "MI_N2012_Sword": [
            0x1AC2,
            0x1E48,
            0xAA36,
            0xADBC
        ],
        "MI_N2012_glass": [
            0x2185,
            0x250B,
            0x25D4,
            0x2601,
            0x263B,
            0x266A,
            0x2697,
            0x26D1,
            0x18879,
            0x18BFF,
            0x18CC8,
            0x18CF5,
            0x18D2F,
            0x18D5E,
            0x18D8B,
            0x18DC5
        ],
        "MI_N2004_body": [
            0x1B4E,
            0x1ED4,
            0x1F9D,
            0x1FCA,
            0x2004,
            0x2033,
            0x2060,
            0x209A,
            0x10E2B,
            0x111B1,
            0x1127A,
            0x112A7,
            0x112E1,
            0x11310,
            0x1133D,
            0x11377
        ],
        "M_Mbs004_all_Inst": [
            0x2185,
            0x250B,
            0x25D4,
            0x2601,
            0x263B,
            0x266A,
            0x2697,
            0x26D1,
            0x1887A,
            0x18C00,
            0x18CC9,
            0x18CF6,
            0x18D30,
            0x18D5F,
            0x18D8C,
            0x18DC6
        ]
    }

def update_portrait_pointer(portrait, portrait_replacement):
    #Simply swap the file's name in the name map and save as the new name
    portrait_replacement_data = UAsset(Manager.asset_dir + "\\" + Manager.file_to_path[portrait_replacement] + "\\" + portrait_replacement + ".uasset", UE4Version.VER_UE4_22)
    index = portrait_replacement_data.SearchNameReference(FString(portrait_replacement))
    portrait_replacement_data.SetNameReference(index, FString(portrait))
    index = portrait_replacement_data.SearchNameReference(FString("/Game/Core/Character/N3100/Material/TextureMaterial/" + portrait_replacement))
    portrait_replacement_data.SetNameReference(index, FString("/Game/Core/Character/N3100/Material/TextureMaterial/" + portrait))
    portrait_replacement_data.Write(Manager.mod_dir + "\\" + Manager.file_to_path[portrait] + "\\" + portrait + ".uasset")

def update_default_outfit_hsv(parameter_string):
    #Set the salon sliders to match the default outfit color
    parameter_list = []
    for index in range(len(parameter_string)//4):
        parameter_list.append(parameter_string[index*4:index*4 + 4])
    for index in range(6):
        for parameter in parameter_list:
            datatable["PB_DT_HairSalonOldDefaults"]["Body_01_" + "{:02d}".format(index + 1)][parameter[0] + "1"] = int(parameter[1:4])

def update_boss_crystal_color():
    #Unlike for regular enemies the crystalization color on bosses does not update to the shard they give
    #So update it manually in the material files
    for file in Manager.file_to_path:
        if Manager.file_to_type[file] == Manager.FileType.Material:
            enemy_id = Manager.file_to_path[file].split("\\")[-2]
            if Enemy.is_boss(enemy_id) or enemy_id == "N2008":
                shard_name = datatable["PB_DT_DropRateMaster"][enemy_id + "_Shard"]["ShardId"]
                shard_type = datatable["PB_DT_ShardMaster"][shard_name]["ShardType"]
                shard_hsv  = shard_type_to_hsv[shard_type.split("::")[-1]]
                set_material_hsv(file, "ShardColor", shard_hsv)

def set_material_hsv(filename, parameter, new_hsv):
    #Change a vector color in a material file
    #Here we use hsv as a base as it is easier to work with
    if Manager.file_to_type[filename] != Manager.FileType.Material:
        raise TypeError("Input is not a material file")
    #Some color properties are not parsed by UAssetAPI and end up in extra data
    #Hex edit in that case
    if filename in material_to_offset:
        for offset in material_to_offset[filename]:
            #Check if given offset is valid
            string = ""
            for num in range(12):
                string += "{:02x}".format(game_data[filename].Exports[0].Extras[offset + num]).upper()
            if string != "0000000000000002FFFFFFFF":
                raise Exception("Material offset invalid")
            #Get rgb
            rgb = []
            for num in range(3):
                list = []
                for index in range(4):
                    list.insert(0, "{:02x}".format(game_data[filename].Exports[0].Extras[offset + 12 + num*4 + index]).upper())
                string = ""
                for index in list:
                    string += index
                rgb.append(struct.unpack("!f", bytes.fromhex(string))[0])
            #Convert
            hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
            if new_hsv[0] < 0:
                new_hue = hsv[0]
            else:
                new_hue = new_hsv[0]/360
            if new_hsv[1] < 0:
                new_sat = hsv[1]
            else:
                new_sat = new_hsv[1]/100
            if new_hsv[2] < 0:
                new_val = hsv[2]
            else:
                new_val = new_hsv[2]/100
            rgb = colorsys.hsv_to_rgb(new_hue, new_sat, new_val)
            #Write rgb
            for num in range(3):
                string = "{:08x}".format(struct.unpack("<I", struct.pack("<f", rgb[num]))[0]).upper()
                list = []
                for index in range(0, len(string), 2):
                    list.insert(0, string[index] + string[index + 1])
                for index in range(4):
                    game_data[filename].Exports[0].Extras[offset + 12 + num*4 + index] = int(list[index], 16)
    #Otherwise change color through the exports
    else:
        for data in game_data[filename].Exports[0].Data:
            if str(data.Name) == "VectorParameterValues":
                for sub_data in data.Value:
                    if str(sub_data.Value[0].Value[0].Value) == parameter:
                        rgb = []
                        rgb.append(sub_data.Value[1].Value[0].Value.R)
                        rgb.append(sub_data.Value[1].Value[0].Value.G)
                        rgb.append(sub_data.Value[1].Value[0].Value.B)
                        hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
                        if new_hsv[0] < 0:
                            new_hue = hsv[0]
                        else:
                            new_hue = new_hsv[0]/360
                        if new_hsv[1] < 0:
                            new_sat = hsv[1]
                        else:
                            new_sat = new_hsv[1]/100
                        if new_hsv[2] < 0:
                            new_val = hsv[2]
                        else:
                            new_val = new_hsv[2]/100
                        rgb = colorsys.hsv_to_rgb(new_hue, new_sat, new_val)
                        sub_data.Value[1].Value[0].Value.R = rgb[0]
                        sub_data.Value[1].Value[0].Value.G = rgb[1]
                        sub_data.Value[1].Value[0].Value.B = rgb[2]

def import_mesh(filename):
    #Import a mesh file at the right location by reading it in the file
    new_file = UAsset("Data\\Mesh\\" + filename + ".uasset", UE4Version.VER_UE4_22)
    name_map = new_file.GetNameMapIndexList()
    filepath = None
    for name in name_map:
        if str(name)[0] == "/" and str(name).split("/")[-1] == filename:
            filepath = str(name)[6:][:-(len(filename)+1)].replace("/", "\\")
            break
    if not filepath:
        raise Exception("Failed to obtain filepath of asset " + filename)
    if not os.path.isdir(Manager.mod_dir + "\\" + filepath):
        os.makedirs(Manager.mod_dir + "\\" + filepath)
    new_file.Write(Manager.mod_dir + "\\" + filepath + "\\" + filename + ".uasset")

def import_texture(filename):
    #Convert DDS to game assets dynamically instead of cooking them within Unreal Editor
    absolute_asset_dir   = os.path.abspath(Manager.asset_dir + "\\" + Manager.file_to_path[filename])
    absolute_texture_dir = os.path.abspath("Data\\Texture")
    absolute_mod_dir     = os.path.abspath(Manager.mod_dir + "\\" + Manager.file_to_path[filename])
    
    root = os.getcwd()
    os.chdir("Tools\\UE4 DDS Tools")
    os.system("cmd /c python\python.exe src\main.py \"" + absolute_asset_dir  + "\\" + filename + ".uasset\" \"" + absolute_texture_dir + "\\" + filename + ".dds\" --save_folder=\"" + absolute_mod_dir + "\" --mode=inject --version=4.22")
    os.chdir(root)
    
    #UE4 DDS Tools does not interrupt the program if a texture fails to convert so do it from here
    if not os.path.isfile(absolute_mod_dir + "\\" + filename + ".uasset"):
        raise FileNotFoundError(filename + ".dds failed to inject")