Import('env')
import os
import shutil

OUTPUT_DIR = "build_output{}".format(os.path.sep)

def bin_map_copy(source, target, env):
    variant = str(target[0]).split(os.path.sep)[2]

    # check if output directories exist and create if necessary
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    for d in ['firmware', 'map']:
        if not os.path.isdir("{}{}".format(OUTPUT_DIR, d)):
            os.mkdir("{}{}".format(OUTPUT_DIR, d))

    # create string with location and file names based on variant
    map_file = "{}map{}{}.map".format(OUTPUT_DIR, os.path.sep, variant)
    bin_file = "{}firmware{}{}.bin".format(OUTPUT_DIR, os.path.sep, variant)

    # check if new target files exist and remove if necessary
    for f in [map_file, bin_file]:
        if os.path.isfile(f):
            os.remove(f)

    # copy firmware.bin to firmware/<variant>.bin
    shutil.copy(str(target[0]), bin_file)

    # move firmware.map to map/<variant>.map
    if os.path.isfile("firmware.map"):
        shutil.move("firmware.map", map_file)

    map_new_loc = str(target[0]).split(os.path.sep)[0] + os.path.sep + str(target[0]).split(os.path.sep)[1] + os.path.sep + str(target[0]).split(os.path.sep)[2] + os.path.sep + "Tasmota.map"
    # move Tasmota.map to map/<variant>.map
    if os.path.isfile(map_new_loc):
        shutil.move(map_new_loc, map_file)

env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", [bin_map_copy])
