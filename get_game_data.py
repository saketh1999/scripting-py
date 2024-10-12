import os  #Operating system
import json #JSON file format
import shutil #Copy files
from subprocess import PIPE, run #Run commands in the terminal
import sys # used to get the command arguments

GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go","build"]

def find_all_game_paths(source):
    game_paths = []
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                game_paths.append(os.path.join(root, directory))
        # break #we only it one time
    
    return game_paths

def compile_game_code(path):
    code_file_name = None
    for root,dir,files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break
        break
    if code_file_name is None:
        return


    command = GAME_COMPILE_COMMAND + [code_file_path]
    run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)

def run_command(command,path):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result.stdout, result.stderr

def make_json_metadata_file(path,game_dirs):
    data = {
        "game_dirs": game_dirs,
        "numberOfGames": len(game_dirs)
    }

    with open(path, "w") as f:
        json.dump(data, f)



def get_name_paths(paths,to_strip):
    new_name = []
    for path in paths:
        _,dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_name.append(new_dir_name)
    return new_name

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def copy_and_overwrite(source, target):
    if os.path.exists(target): #if target exists, delete it
        shutil.rmtree(target)
    shutil.copytree(source, target)


def main(source, target):
    cwd = os.getcwd()
    source_dir = os.path.join(cwd, source) #dont use "" string containations, since path dividers are different in 
                                            #windows and linux
    target_dir = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_dir)
  
    new_game_dirs = get_name_paths(game_paths, "_game")

    create_dir(target_dir)
    
    for src,dest in zip(game_paths,new_game_dirs):
        dest_path = os.path.join(target_dir, dest)
        copy_and_overwrite(src, dest_path)
    
    json_path = os.path.join(target_dir, "metadata.json")
    make_json_metadata_file(json_path,new_game_dirs)

    print(new_game_dirs)



if __name__ == "__main__":
    args = sys.argv 
    if len(args) != 3:
        raise Exception("You must pass a source and target directory - only")
    
    source_dir = args[1]
    target_dir = args[2]

    main(source_dir, target_dir)