import os
import json
from sys import exit
import zipfile


def FileMapper(mode='function', fxnRootDir='', fxnJsonPath='', exts2omit=[]):
    if mode == 'function':
        rootDir = fxnRootDir
        jsonPath = fxnJsonPath
        jsonFilename = os.path.basename(jsonPath)
        try:
            os.chdir(rootDir)
        except:
            print('Unable to change to root directory')
            print('Terminating Session...')
            exit()
        if fxnJsonPath != '':
            if os.path.splitext(jsonFilename)[1] != '.json':
                print('JSON filename does not end with .json')
                print('Terminating Session...')
                exit()
            try:
                fl = len(jsonFilename) + 1
                outputDir = jsonPath[:-fl]
                os.chdir(outputDir)
            except:
                print('Unable to change to output directory')
                print('Terminating Session...')
                exit()

    elif mode == 'terminal':
        rootDir = input('Enter the path of directory to use as the root: ')
        while True:
            if rootDir == 'x':
                print('Terminating Session...')
                exit()
            try:
                os.chdir(rootDir)
                break
            except:
                print('Could not change to root directory')
                rootDir = input('Enter the path of directory to use as the root or enter [x] key to terminate: ')

        jsonPath = input('Define path of the JSON file to be generated (without filename and .json): ')
        while True:
            if jsonPath == 'x':
                print('Terminating Session...')
                exit()
            try:
                os.chdir(jsonPath)
                break
            except:
                print('Could not change to output directory')
                jsonPath = input('Define path of the JSON file to be generated (without filename and .json) or enter '
                                 '[x] key to terminate: ')

        jsonFilename = input('Define filename of the JSON file to be generated (with.json): ')
        while True:
            if jsonPath == 'x':
                print('Terminating Session...')
                exit()
            if os.path.splitext(jsonFilename)[1] != '.json':
                print('JSON filename does not end with .json')
                jsonFilename = input('Define filename of the JSON file to be generated (with.json) or enter [x] key '
                                     'to terminate:')
                continue
            else:
                jsonPath = os.path.join(jsonPath, jsonFilename)
                print(jsonPath)
                break

        is_omitting_exts = False
        while True:
            if not is_omitting_exts:
                extQ = input('Would you like to omit certain file extension from your file map? [y/n]: ')
            if extQ.lower() == 'y':
                extOmission = input('Enter [STOP] to finish or enter a file extension that you would like to omit '
                                    'from your file map (such as .py, .cpp, etc): ')
                is_omitting_exts = True
                if extOmission.upper() == 'STOP':
                    break
                exts2omit.append(str(extOmission))
                print('Omitting ' + extOmission + ' from file map...')
            elif extQ.lower() == 'n':
                print('Including all file extensions')
                break
            else:
                print('Please answer question with [y/n]...')
    else:
        print('mode was not properly define, check spelling.')
        print('The following modes are available:')
        print('function')
        print('terminal')
        exit()

    dict = {}

    l_root = len(rootDir)
    for dir, subdirs, files in os.walk(rootDir):
        for file in files:
            omitFile = False
            isDup = False
            pathNumber = 1
            filename = str(file)
            path = dir[l_root:]

            for extension in exts2omit:
                e = len(file) - len(extension)
                if file[e:] == extension:
                    omitFile = True
            if omitFile:
                continue

            if len(dict) == 0:
                if (jsonPath == '') and (mode == 'function'):
                    fileInfo = {
                        "filename": filename,
                        "number of paths": str(pathNumber),
                        "filepath-" + str(pathNumber): str(path)
                    }
                    dict[filename] = fileInfo
                    print('RUNNING... PLEASE WAIT...')
                    continue
                else:
                    fileInfo = {
                        "filemapper_json": jsonFilename,
                        "filename": filename,
                        "number of paths": str(pathNumber),
                        "filepath-" + str(pathNumber): str(path)
                    }
                    dict[filename] = fileInfo
                    if mode == 'terminal':
                        print('FILEMAPPER RUNNING... PLEASE WAIT...')
                    continue

            else:
                for key in dict:
                    try:
                        if key == filename:
                            pathNumber = int(dict[key]["number of paths"])
                            pathNumber += 1

                            fileInfo = {
                                "number of paths": str(pathNumber),
                                "filepath-" + str(pathNumber): str(path)
                            }
                            isDup = True
                    except:
                        isDup = False

            if not isDup:
                if (jsonPath == '') and (mode == 'function'):
                    fileInfo = {
                        "filename": filename,
                        "number of paths": str(pathNumber),
                        "filepath-" + str(pathNumber): str(path)
                    }
                    dict[filename] = fileInfo
                else:
                    fileInfo = {
                        "filemapper_json": jsonFilename,
                        "filename": filename,
                        "number of paths": str(pathNumber),
                        "filepath-" + str(pathNumber): str(path)
                    }
                    dict[filename] = fileInfo
            else:
                dict[filename]["number of paths"] = str(pathNumber)
                dict[filename]["filepath-" + str(pathNumber)] = str(path)
    if jsonPath != '':
        json_object = json.dumps(dict, indent=4)
        f = open(jsonPath, "w")
        f.write(json_object)
        f.close()

    if mode == 'terminal':
        print('FILEMAPPER RUN COMPLETE')
        print('SAVED ' + str(jsonPath))
    return dict


def Unzip(src, dst):
    with zipfile.ZipFile(src, 'r') as z:
        z.extractall(dst)
