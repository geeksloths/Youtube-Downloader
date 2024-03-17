import os


def get(direction):
    folders = []
    files = get_folders(direction)
    # Get Folders Level 1
    get_folders_level1(direction, files, folders)

    return folders


def get_folders_level1(direction, files, folders):
    for file in files:
        is_folder = check_if_folder(file_name=file)
        if is_folder:
            append(file, folders)
            files = get_folders(direction=direction + "/" + file)
            # Get Folders Level 2
            get_folders_level2(file, files, folders)


def get_folders_level2(file, files, folders):
    for file2 in files:
        is_folder = check_if_folder(file_name=file2)
        if is_folder:
            file2 = file + '/' + file2
            append(file2, folders)


def check_if_folder(file_name):
    result = True
    extracted = len(file_name.split("."))
    if extracted != 1:
        result = False
    return result


def get_folders(direction):
    files = sorted(os.listdir(direction), key=lambda fn: os.path.getctime(os.path.join(direction, fn)))
    return files


def append(file, folders):
    splited_len = len(file.split("."))
    if splited_len == 1:
        if file != "__pycache__":
            folders.append(file)
