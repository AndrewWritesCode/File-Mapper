import os
import tempfile
import zipfile
import json


def FileMapper(root_dir, extensions2omit=None, extensions2include=None):
    if extensions2omit is None:
        extensions2omit = []
    if extensions2include is None:
        extensions2include = []
    file_map = {}
    if not os.path.exists(root_dir):
        raise IsADirectoryError(f'Target path: {root_dir} can\'t be accessed')

    l_root = len(root_dir)
    for directory, sub_directories, files in os.walk(root_dir):
        for file in files:
            omit_file = False
            path_number = 1
            filename = str(file)
            path = directory[l_root:]

            # checks if file has extension that is omitted
            def ext_check(ext):
                if not ext.startswith('.'):
                    ext = f'.{ext}'
                return ext

            # include filter pass
            for extension in extensions2include:
                omit_file = True
                extension = ext_check(extension)
                if os.path.splitext(file)[1] == extension:
                    omit_file = False
                    break

            # exclude filter pass
            for extension in extensions2omit:
                extension = ext_check(extension)
                if os.path.splitext(file)[1] == extension:
                    omit_file = True
                    break
            if omit_file:
                continue

            # checks to see if file_map is empty and initializes if it is
            if not file_map:
                file_info = {
                    "number of paths": path_number,
                    "filepaths": [str(os.path.join(path, filename))]
                }
                file_map[filename] = file_info
            else:
                # either updates file_map for each file of creates new file_map entry
                if filename in file_map:
                    path_number = file_map[filename]["number of paths"]
                    path_number += 1
                    file_map[filename]["number of paths"] = path_number
                    file_map[filename]["filepaths"].append(str(os.path.join(path, filename)))
                else:
                    file_info = {
                        "number of paths": path_number,
                        "filepaths": [str(os.path.join(path, filename))]
                    }
                    file_map[filename] = file_info
    return file_map


def ZipMapper(zip_file, extensions2omit=None, extensions2include=None):
    if os.path.exists(zip_file):
        with zipfile.ZipFile(zip_file) as zf:
            with tempfile.TemporaryDirectory() as temp_dir:
                zf.extractall(temp_dir)
                return FileMapper(temp_dir, extensions2omit=extensions2omit, extensions2include=extensions2include)
    else:
        return


def SmartMapper(path, extensions2omit=None, extensions2include=None):
    if os.path.splitext(path)[1] == ".zip":
        return ZipMapper(path, extensions2omit=extensions2omit, extensions2include=extensions2include)
    else:
        return FileMapper(path, extensions2omit=extensions2omit, extensions2include=extensions2include)


def FileMap2json(file_map, json_path):
    if file_map:
        if os.path.exists(json_path):
            json_object = json.dumps(file_map, indent=4)
            with open(json_path, "w") as j:
                j.write(json_object)


class FileMap:
    def __init__(self, target_path, extensions2omit=None, extensions2include=None):
        self.__root = target_path
        self.__map = SmartMapper(target_path, extensions2omit=extensions2omit, extensions2include=extensions2include)

    @property
    def root(self):
        return self.__root

    @property
    def map(self):
        return self.__map

    def exists(self):
        return bool(self.map)

    def __iter__(self):
        return iter(self.map)

    def __str__(self):
        return f'FileMap Object {self.__name__} maps {self.root}'

    def export_map_to_json(self, json_path):
        if self.map:
            if os.path.exists(json_path):
                json_object = json.dumps(self.map, indent=4)
                with open(json_path, "w") as j:
                    j.write(json_object)
            else:
                print(f'Exporting FileMap Object {self.__name__} to JSON failed: JSON has an invalid output path:\n'
                      f'Invalid path: {json_path}')
        else:
            print(f'Exporting FileMap Object {self.__name__} to JSON failed: has an empty map')
