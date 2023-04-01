import numpy as np


rng = np.random.default_rng()


def rgbToBits(rgb_array: np.array) -> np.array:
    reds = np.clip(rgb_array[:, :, 0], 0, 1)
    return reds.flatten(order='C').astype(int)


def addNoise(bits: np.array, flipChance: float) -> np.array:
    flips = rng.random(size=bits.size) < flipChance
    for i in range(bits.size):
        if flips[i]:
            bits[i] += 1
    return bits % 2


def randomBits(size: int) -> np.array:
    return rng.integers(2, size=size)


## Compression ##

def intToBits(num: int, intSize: int) -> np.array:
    if num // 2**(intSize-1) > 1:
        raise Exception(f'{num} cannot be represented in {intSize} bits')
    result = []
    rem = num
    for i in range(intSize-1, -1, -1):
        quot = rem // 2**i
        rem = rem % 2**i
        result.append(quot)
    return np.array(result)


def bitsToInt(bits: np.array) -> int:
    result = 0
    for i, bit in enumerate(np.flip(bits)):
        result += bit * 2 ** i
    return result


def rlEncode(bits: np.array, intSize: int) -> np.array:
    maxLen = 2**intSize - 1
    result = []
    runLen = 0
    runBit = bits[0]

    for bit in bits:
        if bit != runBit or runLen == maxLen:
            run = intToBits(runLen, intSize)
            result.extend(run)
            result.append(runBit)
            runLen = 1
            runBit = bit
        else:
            runLen += 1
    run = intToBits(runLen, intSize)
    result.extend(run)
    result.append(runBit)

    return np.array(result)


def rlDecode(bits: np.array, intSize: int) -> np.array:
    result = []
    for i in range(0, bits.size, intSize + 1):
        runLen = bitsToInt(bits[i: i+intSize])
        runBit = bits[i + intSize]
        result.extend([runBit] * runLen)
    return np.array(result)


def padBits(bits: np.array, length: int) -> np.array:
    padding = np.zeros(length - bits.size)
    return np.concatenate((bits, padding)).astype(bits.dtype)


def unpadBits(bits: np.array, intSize: int) -> np.array:
    trimmed = np.trim_zeros(bits, trim='b')
    addBack = -trimmed.size % (intSize + 1)
    return np.append(trimmed, [0]*addBack).astype(bits.dtype)
