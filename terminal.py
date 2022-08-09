from fileMapper import FileMapper
from sys import exit
import os
import json


def main():
    cw_dir = os.getcwd()
    root_dir = input('Enter the path of directory to use as the root: ')
    while True:
        if root_dir == 'x':
            print('Terminating Session...')
            exit()
        try:
            os.chdir(root_dir)
            os.chdir(cw_dir)
            break
        except OSError:
            print('Could not change to root directory')
            root_dir = input('Enter the path of directory to use as the root or enter [x] key to terminate: ')

    json_path = input('Define path of the JSON file to be generated (without filename and .json): ')
    while True:
        if json_path == 'x':
            print('Terminating Session...')
            exit()
        try:
            os.chdir(json_path)
            os.chdir(cw_dir)
            break
        except OSError:
            print('Could not change to output directory')
            json_path = input('Define path of the JSON file to be generated (without filename and .json) or enter '
                              '[x] key to terminate: ')

    json_filename = input('Define filename of the JSON file to be generated (with.json): ')
    while True:
        if json_path == 'x':
            print('Terminating Session...')
            exit()
        if os.path.splitext(json_filename)[1] != '.json':
            print('JSON filename does not end with .json')
            json_filename = input('Define filename of the JSON file to be generated (with.json) or enter [x] key '
                                  'to terminate:')
            continue
        else:
            json_path = os.path.join(json_path, json_filename)
            print(json_path)
            break

    try:
        fl = len(json_filename) + 1
        output_dir = json_path[:-fl]
        os.chdir(output_dir)
        os.chdir(cw_dir)
    except OSError:
        print('Unable to change to output directory')
        print('Terminating Session...')
        exit()
    extensions2omit = []
    submitted_ext_omits = False
    ext_question = input('Would you like to omit certain file extension from your file map? [y/n]: ')
    while True:
        if ext_question.lower() == 'y':
            submitted_ext_omits = True
            while True:
                ext_omission = input('Enter [STOP] to finish or enter a file extension that you would like to omit '
                                     'from your file map (such as .py, .cpp, etc): ')
                if ext_omission.upper() == 'STOP':
                    break
                if not ext_omission.startswith('.'):
                    ext_omission = '.' + ext_omission
                extensions2omit.append(str(ext_omission))
                print('Omitting ' + ext_omission + ' from file map...')
        elif ext_question.lower() == 'n':
            print('Including all file extensions')
            break
        else:
            print('Please answer question with [y/n]...')
            input('Would you like to omit certain file extension from your file map? [y/n]: ')
        if submitted_ext_omits:
            break
    print(extensions2omit)
    file_map = FileMapper(root_dir, extensions2omit=extensions2omit)

    json_object = json.dumps(file_map, indent=4)
    f = open(json_path, "w")
    f.write(json_object)
    f.close()

    print('FILEMAPPER RUN COMPLETE')
    print('SAVED ' + str(json_path))


if __name__ == '__main__':
    main()
