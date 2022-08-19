import sys
import os
import tarfile
from pathlib import Path
from compressor import compress_file, decompress_file


slash = str(Path('/'))


#  Загрузка сообщений
msg = list()
with open("messages.txt", 'r', encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        msg.append(line[4:])


def compress(pathLoad: str, pathSave: str=None):
    """Архивирует рекурсивно каталог или файл

    Args:
        pathLoad (str): Пусть до каталога или файла
        pathSave (str, optional): Путь сохранения. По умолчанию сохраняет в той же директории
    """
    if not os.path.exists(pathLoad):
        print(msg[4])
        return -1

    if os.path.isfile(pathLoad):
        if pathSave is None:
            return compress_file(pathLoad, pathLoad + ".faddey")
        else:
            return compress_file(pathLoad, pathSave + ".faddey")

    name = os.path.basename(pathLoad)
    if pathSave is None:
        files = os.listdir(pathLoad)
        for file in files:
            res = compress(pathLoad + slash + file, file)
            if res != 0:
                return res
        directory = os.path.dirname(pathLoad) + slash
        tar = tarfile.open(directory + name + ".faddey", "w:")
        for file in files:
            if os.path.isfile(pathLoad + slash + file):
                file += ".faddey"
            tar.add(file)
            delete_folder(file)
        tar.close()
    else:
        name = os.path.basename(pathLoad)
        os.makedirs(name)
        dirList = os.listdir(pathLoad)
        for name in dirList:
            res = compress(pathLoad + slash + name, pathSave + slash + name)
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


def decompress(pathLoad: str, isFirst: bool=False):
    """Разрхивирует .faddey файл

    Args:
        pathLoad (str): Пусть до .faddey файла
        isFirst (bool, optional): Флаг означающий корень рекурсии. По умолчанию False
    """
    if not os.path.exists(pathLoad):
        print(msg[4])
        return -1

    if os.path.isdir(pathLoad):
        dirList = os.listdir(pathLoad)
        for name in dirList:
            res = decompress(pathLoad + slash + name)
            if res != 0:
                return res
    elif tarfile.is_tarfile(pathLoad):
        extra = ""
        num = 2
        directory = ".".join(pathLoad.split(".")[:-1]) + extra
        while os.path.exists(directory):
            extra = " " + str(num)
            num += 1
            directory = ".".join(pathLoad.split(".")[:-1]) + extra
        tar = tarfile.open(pathLoad)
        tar.extractall(".".join(pathLoad.split(".")[:-1]) + extra)
        tar.close()
        return decompress(directory)
    else:
        if isFirst:
            extra = ""
            num = 2
            temp = pathLoad.split(".")
            path = ".".join(temp[:-2]) + extra + "." + temp[-2:-1][0]
            while os.path.exists(path):
                extra = " " + str(num)
                num += 1
                temp = pathLoad.split(".")
                path = ".".join(temp[:-2]) + extra + "." + temp[-2:-1][0]
            res = decompress_file(pathLoad, path)
        else:
            res = decompress_file(pathLoad, ".".join(pathLoad.split(".")[:-1]))
            os.remove(pathLoad)
        return res
    return 0


a = sys.argv
if len(a) == 1:
    print(msg[0])
elif a[1] == "help":
    print(msg[2])
    print(msg[3])
elif a[1] == "compress":
    res = compress(" ".join(a[2:]))
    if res == 0:
        print("Done")
    else:
        print("Error")
elif a[1] == "decompress":
    res = decompress(" ".join(a[2:]), True)
    if res == 0:
        print("Done")
    else:
        print("Error")
else:
    print(msg[1])
    print(msg[0])
