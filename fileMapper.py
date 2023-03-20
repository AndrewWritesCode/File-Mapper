import os
import tempfile
import zipfile
from warnings import warn


def FileMapper(root_dir, extensions2omit=None, extensions2include=None):
    if extensions2omit is None:
        extensions2omit = []
    if extensions2include is None:
        extensions2include = []
    file_map = {}
    if not os.path.exists(root_dir):
        warn(f"FileMap not created. Unable to access target root directory: {root_dir}")
        return

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
