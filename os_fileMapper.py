import os


def path2list(filepath):
    path_list = []
    split = os.path.split(filepath)
    path_list.append(split[1])
    while True:
        split = os.path.split(split[0])
        if split[1] == '':
            break
        path_list.append(split[1])
    path_list.append(split[0])
    path_list.reverse()
    return path_list


def list2path(filepath_list):
    if len(filepath_list) == 1:
        return os.path.normpath(filepath_list[0])
    else:
        filepath = os.path.join(filepath_list[0], filepath_list[1])
        if len(filepath_list) == 2:
            return filepath
    for i in range(2, len(filepath_list)):
        filepath = os.path.join(filepath, filepath_list[i])
    return filepath


def substitute_path(orig_path, sub_path, filepath):
    orig_list = path2list(orig_path)
    sub_list = path2list(sub_path)
    filepath_list = path2list(filepath)

    for i in range(len(filepath_list)):
        if filepath_list[i] == orig_list[0]:
            j = i + 1
            for k in range(1, len(orig_list)+1):
                if k == len(orig_list):
                    out_path = filepath_list[:i] + sub_list + filepath_list[(i+len(orig_list)):]
                    return list2path(out_path)
                if filepath_list[j] != orig_list[k]:
                    break
                j += 1
    return filepath


def substitute_filename_in_path(orig_filename, sub_filename, filepath, keep_ext=True):
    name = os.path.split(filepath)
    if name[1] != orig_filename:
        return filepath
    else:
        if not keep_ext:
            return os.path.join(name[0], sub_filename)
        else:
            ext = os.path.splitext(name[1])[1]
            name_only = os.path.splitext(sub_filename)[0]
            return os.path.join(name[0], f'{name_only}{ext}')
