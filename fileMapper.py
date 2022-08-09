import os
from sys import exit
import zipfile


def Unzip(src, dst):
    with zipfile.ZipFile(src, 'r') as z:
        z.extractall(dst)


def FileMapper(root_dir, extensions2omit=[]):
    file_map = {}
    if not os.path.exists(root_dir):
        print('Unable to change to root directory')
        print('Terminating Session...')
        exit()

    l_root = len(root_dir)
    for directory, sub_directories, files in os.walk(root_dir):
        for file in files:
            omit_file = False
            path_number = 1
            filename = str(file)
            path = directory[l_root:]

            # checks if file has extension that is omitted
            for extension in extensions2omit:
                if not extension.startswith('.'):
                    extension = '.' + extension
                if os.path.splitext(file)[1] == extension:
                    omit_file = True
                    break
            if omit_file:
                continue

            # checks to see if file_map is empty and initializes if it is
            if not file_map:
                file_info = {
                    "filename": filename,
                    "number of paths": path_number,
                    "filepath-" + str(path_number): str(path)
                }
                file_map[filename] = file_info
            else:
                # either updates file_map for each file of creates new file_map entry
                if filename in file_map:
                    path_number = file_map[filename]["number of paths"]
                    path_number = path_number + 1
                    file_map[filename]["number of paths"] = path_number
                    file_map[filename]["filepath-" + str(path_number)] = str(path)
                else:
                    file_info = {
                        "filename": filename,
                        "number of paths": path_number,
                        "filepath-" + str(path_number): str(path)
                    }
                    file_map[filename] = file_info
    return file_map
