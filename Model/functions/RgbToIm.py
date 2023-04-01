import os
from typing import NewType
from nptyping import NDArray, UInt8, Shape
from PIL import Image
import numpy as np


rgb = NewType('rgb', NDArray[Shape['*, *, 3'], UInt8])
fileName = NewType('fileName', str)

## File Name Tools ##

imageExts = ['.jpg', '.jpeg', '.png', '.gif', '.webp',
             '.tif', '.tiff', '.raw', '.bmp', 'heif',
             '.ind', '.indd', '.jp2', '.j2k', '.svg',
             '.ai', '.esp', '.pdf']


def getExt(name: fileName) -> str:
    subStrs = name.split('.')
    if len(subStrs) > 1 and subStrs[0] != '':
        return f'.{subStrs[-1]}'
    else:
        return ''


def hasImageExt(string: str) -> bool:
    return getExt(string) in imageExts

## Saving Data ##


def saveImage(rgb_array: rgb, name: fileName, path: str = '') -> None:
    if not hasImageExt(name):
        name = name + '.png'
    start = os.getcwd()
    os.chdir(f'{start}/{path}')
    image = Image.fromarray(rgb_array.astype(np.uint8), mode='RGB')
    image.save(name)
    os.chdir(start)


def saveImages(oneBits: list, path: str) -> None:
    for i, rgb_array in enumerate(oneBits):
        saveImage(rgb_array, f'{i}', path)


def saveGif(trgb_array: rgb, name: str, path: str = '', fps: int = 30) -> None:
    start = os.getcwd()
    os.chdir(f'{start}/{path}')
    nFrames = trgb_array.shape[0]
    duration = nFrames / fps
    imageList = [Image.fromarray(trgb_array[t, :, :, :])
                 for t in range(nFrames)]
    imageList[0].save(f'{name}.gif', save_all=True,
                      append_images=imageList[1:], optimize=False, duration=nFrames / fps, loop=0)
    os.chdir(start)
