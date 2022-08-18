import sys
import os
from pathlib import Path
from compressor import compress_file, decompress_file


slash = str(Path('/'))


#  Загрузка сообщений
msg = list()
with open("messages.txt", 'r', encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        msg.append(line[4:])


def compress(path: str):
    dir, name, ext = get_file_info(path)
    if dir == -1:
        return -1

    compress_file(path, dir + name)
    

def decompress(path: str):
    dir, name, ext = get_file_info(path)
    if dir == -1:
        return -1

    decompress_file(path, dir + name)
    
    
def get_file_info(path: str):
    """Разбивает ссылку на 3 части - директория, имя файла, расширение файла 

    Args:
        path (str): Путь
    """
    if not os.path.exists(path):
        print(msg[4])
        return -1, -1, -1

    directory = os.path.dirname(path)
    file = path[len(directory) + 1:].split('.')
    if len(file) == 1:
        return directory + slash, file[0], "dir"
    return directory + slash, file[0], file[1]


a = sys.argv
a = ['main.py', 'compress', '/Users/faddey/Desktop/untitled folder']
if len(a) == 1:
    print(msg[0])
elif a[1] == "help":
    print(msg[2])
    print(msg[3])
elif a[1] == "compress":
    compress(" ".join(a[2:]))
elif a[1] == "decompress":
    decompress(" ".join(a[2:]))
else:
    print(msg[1])
    print(msg[0])