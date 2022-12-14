import bitarray
import os


def compress_file(load_path: str, save_path: str):
    """Архивирует файл

    Args:
        pathLoad (str): Путь до файла
        pathSave (str): Путь сохранения
    """
    file_name = os.path.basename(load_path)
    
    with open(load_path, 'rb') as f:
        bytes = bytearray(f.read())

    if len(bytes) == 0:
        with open(save_path, 'wb') as f:
            return 0
        
    hash_code = abs(hash(frozenset(bytes)))
    hash_code = decimal_to_binary(hash_code)
    
    if len(hash_code) < 30:
        hash_code += "0" * (30 - len(hash_code))
    else:
        hash_code = hash_code[:30]

    next_code = 0
    dictionary = dict()
    for i in range(256):
        dictionary[(i,)] = next_code
        next_code += 1

    group = ()
    encoded = list()
    for byte in bytes:
        current = group + (byte,)
        if current in dictionary:
            group = current
        else:
            encoded.append(dictionary[group])
            dictionary[current] = next_code
            next_code += 1
            group = (byte,)
    encoded.append(dictionary[group])

    bit_depth = len(decimal_to_binary(len(dictionary) - 1))
    bit_depth_2 = decimal_to_binary(bit_depth)
    bites = "0" * (8 - len(bit_depth_2)) + bit_depth_2

    for i in encoded:
        dv = decimal_to_binary(i)
        left = "0" * (bit_depth - len(dv))
        bites += (left + dv)

    bit_arr = bitarray.bitarray(hash_code + bites)

    with open(save_path, 'wb') as f:
        f.write(bit_arr)
        
    k = os.path.getsize(save_path) / os.path.getsize(load_path)
    k *= 100
        
    print(f"Процент сжатия {file_name} = {k}")

    return 0


def decimal_to_binary(n: int):
    """Переводит число из десятичной в двоичную систему

    Args:
        n (int): Десятичное число

    Returns:
        str: Двоичное число
    """
    result = ""
    while n >= 2:
        result += str(n % 2)
        n = n // 2
    result += str(n)
    return result[::-1]


def decompress_file(load_path: str, save_path: str):
    """Разархивирует файл

    Args:
        pathLoad (str): Путь до файла
        pathSave (str): Путь сохранения
    """
    bites = bitarray.bitarray()
    with open(load_path, 'rb') as f:
        bites.fromfile(f)
        
    hash_code_input = str(bites[:30])
    hash_code_input = hash_code_input[10:]
    hash_code_input = hash_code_input[:-2]
    
    bites = bites[30:]

    if len(bites) == 0:
        with open(save_path, 'wb') as f:
            return 0

    bit_depth = int(binary_to_decimal(str(bites[0:8])[10:-2]))
    a = (len(bites) - 8) - ((len(bites) - 8) // bit_depth) * bit_depth
    if a != 0:
        bites = bites[8:-a]
    else:
        bites = bites[8:]
    count = 0
    current = ""
    encoded = list()
    for bit in bites:
        if count < bit_depth:
            current += str(bit)
            count += 1
        else:
            encoded.append(binary_to_decimal(current))
            current = str(bit)
            count = 1
    encoded.append(binary_to_decimal(current))

    bytes = list()

    next_code = 0
    dictionary = dict()
    for i in range(256):
        dictionary[next_code] = (i,)
        next_code += 1

    previous_code = -1
    for code in encoded:
        if previous_code == -1:
            bytes += dictionary[code]
            previous_code = code
            continue
        if code in dictionary:
            bytes += dictionary[code]
            value = dictionary[previous_code] + (dictionary[code][0],)
            dictionary[next_code] = value
        else:
            s = dictionary[previous_code] + (dictionary[previous_code][0],)
            bytes += s
            dictionary[next_code] = s
        next_code += 1
        previous_code = code
    
    hash_code = abs(hash(frozenset(bytes)))   
    hash_code = decimal_to_binary(hash_code)[:30]
    
    if hash_code != hash_code_input:
        raise "Файл был повреждён"
    
    with open(save_path, "wb") as f:
        f.write(bytearray(bytes))
    return 0


def binary_to_decimal(s: str):
    """Переводит число из двоичной в десятичную систему

    Args:
        s (str): Двоичное число

    Returns:
        int: Десятичное число
    """
    s = s[::-1]
    result = 0
    power = 0
    for i in s:
        if i == "1":
            result += 2 ** power
        power += 1
    return result
