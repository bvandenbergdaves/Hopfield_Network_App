import numpy as np
import math
from imToRgb import getImageTiles, getImages, removeExt
from RgbToBits import rgbToBits
from patternFiltering import filterSiblings
from RgbToIm import saveImage
import rgbArrays as rgb


## Arg Dicts ##
def makeCompDict(path: str = 'imported', targetPx: int = 160000) -> dict[np.array, int]:
    arrayDict = getImages(path, asDict=True)
    pxSizeDict = dict()
    for name, array in arrayDict.items():
        pxSizeDict[name] = math.ceil(math.sqrt(array.size / targetPx))
    return pxSizeDict


def makeConstDict(value, path: str = 'imported') -> dict[np.array, int]:
    arrayDict = getImages(path, asDict=True)
    pxSizeDict = dict()
    for name, array in arrayDict.items():
        pxSizeDict[name] = value
    return pxSizeDict


## Application ##
def applyToAll(func: 'function', nameMod: str, args: dict = None, path0='imported', path1='processed'):
    arrayDict = getImages(path0, asDict=True)
    editedDict = dict()
    if args is None:
        for name, array in arrayDict.items():
            print(name)
            editedDict[name] = func(array)
    elif not isinstance(args, dict):
        for name, array in arrayDict.items():
            print(name)
            editedDict[name] = func(array, args)
    else:
        for name, array in arrayDict.items():
            print(name)
            editedDict[name] = func(array, args[name])

    for name, array in editedDict.items():
        saveImage(array, ''.join([removeExt(name), f'{nameMod}']), path1)


def cropAll(path0='imported', path1='processed'):
    arrayDict = getImages(path0, asDict=True)
    editedDict = dict()
    for name, array in arrayDict.items():
        print(
            f'{name} has a resolution of {array.shape[0]} X {array.shape[1]}')
        t, b = input('remove from top:'), input('remove from top:')
        l, r = input('remove from left:'), input('remove from right:')
        editedDict[name] = rgb.marginCrop(array, (t, b, l, r))
    for name, array in editedDict.items():
        saveImage(array, ''.join([removeExt(name), f'_cropped']), path1)


## Analysis ##
def findNumPatterns(path: str, shape: tuple[int] = (100, 100), cutoff: float = 0.4) -> None:
    rgb_arrays = getImageTiles(path, shape)
    tiles = list(map(rgbToBits, rgb_arrays))
    print(f'{path} generated {len(tiles)} {shape[0]} X {shape[1]} tiles')
    patterns = filterSiblings(tiles, cutoff)
    print(f'{len(patterns)} of them can be used as patterns with a hebb cutoff of {cutoff}')
