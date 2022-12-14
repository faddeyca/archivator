import sys
import os
import tarfile
import pathlib
from compressor import compress_file, decompress_file


slash = str(pathlib.Path('/'))


#  Загрузка сообщений
msg = list()
with open("messages.txt", 'r', encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        msg.append(line[4:])


def compress(load_path: str, save_path: str=None):
    """Архивирует рекурсивно каталог или файл

    Args:
        pathLoad (str): Путь до каталога или файла
        pathSave (str, optional): Путь сохранения. По умолчанию сохраняет в той же директории
    """
    if not os.path.exists(load_path):
        print(msg[5])
        return -1

    if os.path.isfile(load_path):
        if save_path is None:
            return compress_file(load_path, load_path + ".faddey")
        else:
            return compress_file(load_path, save_path + ".faddey")

    name = os.path.basename(load_path)
    if save_path is None:
        files = os.listdir(load_path)
        for file in files:
            res = compress(load_path + slash + file, file)
            if res != 0:
                return res
        directory = os.path.dirname(load_path) + slash
        tar = tarfile.open(directory + name + ".faddey", "w:")
        for file in files:
            if os.path.isfile(load_path + slash + file):
                file += ".faddey"
            tar.add(file)
            delete_folder(file)
        tar.close()
    else:
        name = os.path.basename(load_path)
        os.makedirs(name)
        dirList = os.listdir(load_path)
        for name in dirList:
            res = compress(load_path + slash + name, save_path + slash + name)
            if res != 0:
                return res
    return 0


def delete_folder(path: str):
    """Удаляет каталог

    Args:
        path (str): Путь до каталога
    """
    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            delete_folder(path + slash + file)
        os.rmdir(path)
    else:
        os.remove(path)


def decompress(load_path: str, is_first: bool=False):
    """Разрхивирует .faddey файл

    Args:
        pathLoad (str): Пусть до .faddey файла
        isFirst (bool, optional): Флаг означающий корень рекурсии. По умолчанию False
    """
    if not os.path.exists(load_path):
        print(msg[5])
        return -1

    if os.path.isdir(load_path):
        dirList = os.listdir(load_path)
        for name in dirList:
            res = decompress(load_path + slash + name)
            if res != 0:
                return res
    elif tarfile.is_tarfile(load_path):
        extra = ""
        num = 2
        directory = ".".join(load_path.split(".")[:-1]) + extra
        while os.path.exists(directory):
            extra = " " + str(num)
            num += 1
            directory = ".".join(load_path.split(".")[:-1]) + extra
        tar = tarfile.open(load_path)
        tar.extractall(".".join(load_path.split(".")[:-1]) + extra)
        tar.close()
        return decompress(directory)
    else:
        if is_first:
            extra = ""
            num = 2
            temp = load_path.split(".")
            path = ".".join(temp[:-2]) + extra + "." + temp[-2:-1][0]
            while os.path.exists(path):
                extra = " " + str(num)
                num += 1
                temp = load_path.split(".")
                path = ".".join(temp[:-2]) + extra + "." + temp[-2:-1][0]
            res = decompress_file(load_path, path)
        else:
            res = decompress_file(load_path, ".".join(load_path.split(".")[:-1]))
            os.remove(load_path)
        return res
    return 0    
    
    
a = sys.argv
if len(a) == 1:
    print(msg[0])
elif a[1] == "help":
    print(msg[2])
    print(msg[3])
    print(msg[4])
elif a[1] == "compress":
    res = compress(os.path.abspath(" ".join(a[2:])))
    if res == 0:
        print("Done")
    else:
        print("Error")
elif a[1] == "decompress":
    res = decompress(os.path.abspath(" ".join(a[2:])), True)
    if res == 0:
        print("Done")
    else:
        print("Error")
elif a[1] == "list":
    file = tarfile.open(os.path.abspath(" ".join(a[2:])))
    members = file.getmembers()
    for member in members:
        name = member.name
        print(" -- " * (name.count(slash) + 1) +
              name.split(slash)[-1].split(".faddey")[0])
else:
    print(msg[1])
    print(msg[0])
