import bitarray


def compress_file(pathLoad: str, pathSave: str):
    """Архивирует файл

    Args:
        pathLoad (str): Путь до файла
        pathSave (str): Путь сохранения
    """
    with open(pathLoad, "rb") as f:
        bytes = bytearray(f.read())

    nextCode = 0
    dictionary = dict()
    for i in range(256):
        dictionary[(i,)] = nextCode
        nextCode += 1

    group = ()
    encoded = list()
    for byte in bytes:
        current = group + (byte,)
        if current in dictionary:
            group = current
        else:
            encoded.append(dictionary[group])
            dictionary[current] = nextCode
            nextCode += 1
            group = (byte,)
    encoded.append(dictionary[group])

    bitDepth = len(decimal_to_binary(len(dictionary) - 1))
    bitDepth2 = decimal_to_binary(bitDepth)
    bites = "0" * (8 - len(bitDepth2)) + bitDepth2

    for i in encoded:
        dv = decimal_to_binary(i)
        left = "0" * (bitDepth - len(dv))
        bites += (left + dv)

    bitarr = bitarray.bitarray(bites)

    with open(pathSave, 'wb') as f:
        f.write(bitarr)


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


def decompress_file(pathLoad: str, pathSave: str):
    """Разархивирует файл

    Args:
        pathLoad (str): Путь до файла
        pathSave (str): Путь сохранения
    """
    bites = bitarray.bitarray()
    with open(pathLoad, 'rb') as f:
        bites.fromfile(f)

    bitDepth = int(binary_to_decimal(str(bites[0:8])[10:-2]))
    a = (len(bites) - 8) - ((len(bites) - 8) // bitDepth) * bitDepth
    if a != 0:
        bites = bites[8:-a]
    else:
        bites = bites[8:]
    count = 0
    current = ""
    encoded = list()
    lol = 0
    for bit in bites:
        lol += 1
        if count < bitDepth:
            current += str(bit)
            count += 1
        else:
            encoded.append(binary_to_decimal(current))
            current = str(bit)
            count = 1
    encoded.append(binary_to_decimal(current))

    bytes = list()

    nextCode = 0
    dictionary = dict()
    for i in range(256):
        dictionary[nextCode] = (i,)
        nextCode += 1

    previousCode = -1
    for code in encoded:
        if previousCode == -1:
            bytes += dictionary[code]
            previousCode = code
            continue
        if code in dictionary:
            bytes += dictionary[code]
            value = dictionary[previousCode] + (dictionary[code][0],)
            dictionary[nextCode] = value
        else:
            s = dictionary[previousCode] + (dictionary[previousCode][0],)
            bytes += s
            dictionary[nextCode] = s
        nextCode += 1
        previousCode = code
    with open(pathSave, "wb") as f:
        f.write(bytearray(bytes))


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
