import os
from PIL import Image
from typing import NewType
from nptyping import NDArray, UInt8, Shape
import numpy as np
import os

## File Name Tools ##

rgb = NewType('rgb', NDArray[Shape['*, *, 3'], UInt8])
fileName = NewType('fileName', str)


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

def hasImageExt(string: str) -> bool:
    imageExts = ['.jpg', '.jpeg', '.png', '.gif', '.webp',
                 '.tif', '.tiff', '.raw', '.bmp', 'heif',
                 '.ind', '.indd', '.jp2', '.j2k', '.svg',
                 '.ai', '.esp', '.pdf']
    return getExt(string) in imageExts

def getImageNames(path: str = '', keepExt: bool = True) -> list[fileName]:
    names = filter(hasImageExt, os.listdir(path))
    if keepExt:
        return list(names)
    else:
        return [removeExt(name) for name in names]

def saveImage(rgb_array: rgb, name: fileName, path: str = '') -> None:
    if not hasImageExt(name):
        name = name + '.png'
    start = os.getcwd()
    os.chdir(f'{start}/{path}')
    image = Image.fromarray(rgb_array.astype(np.uint8), mode='RGB')
    image.save(name)
    os.chdir(start)

def display_contents(line_limit: int, start: int = 0) -> None:
    print('Files and Folders in ', os.getcwd())

def display_list(header: str, lst: list, line_limit: int) ->None:
    print(header)
    for i, object in enumerate(lst):
        if  i % (line_limit + 1) < line_limit:
            print(object)
        else:
            print('...\n')
            option = input('Press ENTER to conitue or Q to quit: ')
            option.upper()
            if option == 'Q':
                break
            else:
                os.system('clear')
                display_list(header,lst[i:],line_limit)
                break

if __name__ == '__main__':
    pass

