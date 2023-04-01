from PIL import Image
from typing import NewType, Tuple
from nptyping import NDArray, UInt8, Shape
import numpy as np
import os

## File Name Tools ##

rgb = NewType('rgb', NDArray[Shape['*, *, 3'], UInt8])
fileName = NewType('fileName', str)

imageExts = ['.jpg', '.jpeg', '.png', '.gif', '.webp',
             '.tif', '.tiff', '.raw', '.bmp', 'heif',
             '.ind', '.indd', '.jp2', '.j2k', '.svg',
             '.ai', '.esp']


def getExt(name: fileName) -> str:
    subStrs = name.split('.')
    if len(subStrs) > 1 and subStrs[0] != '':
        return f'.{subStrs[-1]}'
    else:
        return ''


def removeExt(name: fileName) -> str:
    extLen = len(getExt(name))
    if extLen == 0:
        return name
    else:
        return name[:-extLen]


def hasImageExt(name: fileName) -> bool:
    return getExt(name) in imageExts


def getImageNames(path: str = '', keepExt: bool = True) -> list[fileName]:
    names = filter(lambda file: hasImageExt(file), os.listdir(path))
    if keepExt:
        return list(names)
    else:
        return list(map(removeExt, names))


## Single Image ##

def getImage(name: fileName, path: str = '') -> rgb:
    names = getImageNames(path)
    start = os.getcwd()
    os.chdir(f'{start}/{path}')
    for file in names:
        if file.startswith(name) and any([file.endswith(ext) for ext in imageExts]):
            image = Image.open(name).convert(mode='RGB')
            os.chdir(start)
            return rgb(np.asarray(image).astype(np.uint8))
    else:
        raise Exception(f'there is no image file named {name} in {path}')


## Multiple Images ##

def getImages(path: str, asDict: bool = False) -> list[rgb] | dict[fileName, rgb]:
    names = getImageNames(path)
    images = []
    start = os.getcwd()
    os.chdir(f'{start}/{path}')
    for name in names:
        image = Image.open(name).convert(mode='RGB')
        images.append(rgb(np.asarray(image).astype(np.uint8)))
    os.chdir(start)

    return dict(zip(names, images)) if asDict else images


def tiles(rgb_array: rgb, shape: Tuple[int, int]) -> list[rgb]:
    h0, w0 = rgb_array.shape[:2]
    h1, w1 = shape
    y, x = 0, 0
    tile_arrays = []
    while y + h1 <= h0:
        while x + w1 <= w0:
            tile_arrays.append(rgb(rgb_array[y: y+h1, x: x+w1, :]))
            x += w1
        x = 0
        y += h1
    return tile_arrays


def getImageTiles(path: str, shape: Tuple[int, int]) -> list[rgb]:
    images = getImages(path)
    cropped = []
    for image in images:
        cropped.extend(tiles(image, shape))
    return cropped
