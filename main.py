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
            compress(pathLoad + slash + file, file)
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
            compress(pathLoad + slash + name, pathSave + slash + name)
    return 0


def delete_folder(path: str):
    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            delete_folder(path + slash + file)
        os.rmdir(path)
    else:
        os.remove(path)
    

def decompress(pathLoad: str, pathSave: str=None):
    if not os.path.exists(pathLoad):
        print(msg[4])
        return -1

    if os.path.isdir(pathLoad):
        dirList = os.listdir(pathLoad)
        for name in dirList:
            decompress(pathLoad + slash + name)
    elif tarfile.is_tarfile(pathLoad):
        extra = ""
        num = 2
        directory = ""
        while True:
            try:
                directory = "".join(pathLoad.split(".")[:-1]) + extra
                os.makedirs(directory)
                break
            except:
                extra = " " + str(num)
                num += 1
        tar = tarfile.open(pathLoad)
        tar.extractall("".join(pathLoad.split(".")[:-1]) + extra)
        tar.close()
        decompress(directory)
    else:
        decompress_file(pathLoad, ".".join(pathLoad.split(".")[:-1]))
        os.remove(pathLoad)
    return 0


a = sys.argv
a = ['main.py', 'compress', '/Users/faddey/Desktop/untitled folder']
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
    res = decompress(" ".join(a[2:]))
    if res == 0:
        print("Done")
    else:
        print("Error")
else:
    print(msg[1])
    print(msg[0])
