from typing import NewType, Tuple
from nptyping import NDArray, UInt8, Shape
import math
import numpy as np


rng = np.random.default_rng()

rgb = NewType('rgb', NDArray[Shape['*, *, 3'], UInt8])
color = NewType('color', NDArray[Shape['3'], UInt8])


## Analysis ##


def isGreyscale(image: rgb) -> bool:
    return np.unique(image, axis=2).shape[2] == 1


def isOneBit(image: rgb) -> bool:
    return isGreyscale(image) and len(np.unique(image[:, :, 0])) <= 2


## Data Conversion ##

def bitsToRgb(bits: np.array, shape: Tuple[int, int]) -> rgb:
    values = ((bits + 1) % 2 * 255).astype(np.uint8)
    reds = values.reshape(shape)
    return np.stack([reds, reds, reds], axis=2)


## Cropping ##

def shapeCrop(image: rgb, width: int, height:int, refPt: str = 'top_left') -> rgb:
    h0, w0 = image.shape[:2]
    h1, w1 = min(height, h0), min(width, w0)
    match refPt:
        case 'top left':
            return image[:h1, :w1, :]
        case 'top right':
            return image[:h1, w0-w1:, :]
        case 'bottom left':
            return image[h0-h1:, :w1, :]
        case 'bottom right':
            return image[h0-h1:, w0-w1:, :]
        case 'center':
            t, b = math.floor((h0 - h1)/2), math.ceil((h0 - h1)/2)
            l, r = math.floor((w0 - w1)/2), math.ceil((w0 - w1)/2)
            return image[t:h0-b, l:w0-r, :]
        case _:
            raise Exception(
                r"The refPt argument in crop(image, shape, refPt) must be one of: 'top_left', 'top_right', 'bottom_left', 'bottom_right', or 'center'")


def shapePtCrop(image: rgb, shape: Tuple[int, int], refPt: Tuple[int, int] = (0, 0)) -> rgb:
    y, x = refPt
    h0, w0 = image.shape[:2]
    h1, w1 = min(shape[0], h0 - y), min(shape[1], w0 - x)
    return image[y: y + h1, x: x + w1:]


def marginCrop(image: rgb, margins: Tuple[int, int]) -> rgb:
    h, w = image.shape[:2]
    t, b, l, r = margins
    return image[t:h-b, l:w-r, :]


def tiles(image: rgb, shape: Tuple[int, int]) -> list[rgb]:
    h0, w0 = image.shape[:2]
    h1, w1 = shape
    y, x = 0, 0
    tile_arrays = []
    while y + h1 <= h0:
        while x + w1 <= w0:
            tile_arrays.append(rgb(image[y: y+h1, x: x+w1, :]))
            x += w1
        x = 0
        y += h1
    return tile_arrays


## Compression ##

def compress(image: rgb, pxSize: int, refPt: Tuple[int, int] = (0, 0)) -> rgb:
    h0, w0 = image.shape[:2]
    h1, w1 = h0 // pxSize, w0 // pxSize
    image = shapePtCrop(image, (h1*pxSize, w1*pxSize), refPt=refPt)
    new_array = np.zeros((h1, w1, 3))
    for i in range(h1):
        for j in range(w1):
            y0, y1 = i * pxSize, (i+1) * pxSize
            x0, x1 = j * pxSize, (j+1) * pxSize
            new_array[i, j, :] = np.round(
                np.mean(image[y0:y1, x0:x1, :], axis=(0, 1)))
    return new_array.astype(np.uint8)


def oneBitCompress(image: rgb, pxSize: int, refPt: Tuple[int, int] = (0, 0)) -> rgb:
    h0, w0 = image.shape[:2]
    h1, w1 = h0 // pxSize, w0 // pxSize
    image = shapeCrop(image, (h1*pxSize, w1*pxSize), refPt=refPt)

    new_array = np.zeros((h1, w1, 3))
    for i in range(h1):
        for j in range(w1):
            y0, y1 = i * pxSize, (i+1) * pxSize
            x0, x1 = j * pxSize, (j+1) * pxSize
            if len(np.flatnonzero(image[y0:y1, x0:x1, 0])) > (y1-y0) * (x1-x0) / 2:
                new_array[i, j, :] = 255
            else:
                new_array[i, j, :] = 0
    return new_array.astype(np.uint8)


def continuousScale(image: rgb, factor: float) -> rgb:
    nPrints = 0

    pxSize = 1/factor
    h0, w0 = image.shape[:2]
    h1, w1 = int(h0 * factor), int(w0 * factor)
    new_array = np.zeros((h1, w1, 3))
    for i in range(h1):
        for j in range(w1):
            y0, y1 = i * pxSize, (i+1) * pxSize
            x0, x1 = j * pxSize, (j+1) * pxSize

            t, b, l, r = -y0 % 1, y1 % 1, -x0 % 1, x1 % 1

            y0, y1 = math.ceil(y0), math.floor(y1)
            x0, x1 = math.ceil(x0), math.floor(x1)
            h, w = y1 - y0, x1 - x0

            weightedSum = np.array([0.0, 0.0, 0.0])
            top, bottom, left, right, width, height = tuple(
                map(lambda x: x > 0, [t, b, l, r, w, h]))

            # Middle
            if width and height:
                weightedSum += np.sum(image[y0:y1, x0:x1, :],
                                      axis=(0, 1))
            # Edges
            if width:
                if top:
                    weightedSum += np.sum(image[y0 - 1, x0:x1, :],
                                          axis=(0, 1)) * t
                if bottom:
                    weightedSum += np.sum(image[y1, x0:x1, :],
                                          axis=(0, 1)) * b
            if height:
                if left:
                    weightedSum += np.sum(image[y0:y1, x0 - 1, :],
                                          axis=(0, 1)) * l
                if right:
                    weightedSum += np.sum(image[y0:y1, x1, :],
                                          axis=(0, 1)) * r
            # Corners
            if top:
                if left:
                    weightedSum += t * l * \
                        image[y0 - 1, x0 - 1, :]
                if right:
                    weightedSum += t * r * \
                        image[y0 - 1, x1, :]
            if bottom:
                if left:
                    weightedSum += b * l * \
                        image[y1, x0 - 1, :]
                if right:
                    weightedSum += b * r * image[y1, x1, :]

            new_array[i, j, :] = np.round(weightedSum / (pxSize ** 2))
            if nPrints < 26:
                nPrints += 1
                print(i, j, t, b, l, r, w, h)
                print(weightedSum)
                print(np.round(weightedSum / (pxSize ** 2)))

    return new_array.astype(np.uint8)


def scaleToTarget(image: rgb, target: int, mode: str = 'smallest dimension') -> rgb:
    h, w = image.shape[:2]
    match mode:
        case 'size':
            factor = math.sqrt(target / (w * h))
        case 'width':
            factor = target / w
        case 'height':
            factor = target / h
        case 'smallest dimension':
            factor = target / min(w, h)
        case _:
            raise Exception(
                f'{mode} is not a recognised mode for scaleToTarget')
    return continuousScale(image, round(factor, ndigits=3))


def scaleUp(image: rgb, scale: int) -> rgb:
    return np.kron(image, np.ones((scale, scale, 1))).astype(np.uint8)


## Color Conversion ##

def toGreyscale(image: rgb) -> rgb:
    flat_array = np.round((np.mean(image, axis=2)))
    return np.stack((flat_array, flat_array, flat_array), axis=2)


def toOneBitMedian(image: rgb) -> rgb:
    flat_array = np.round((np.mean(image, axis=2)))
    cutoff = np.median(flat_array)
    bitArray = (flat_array >= cutoff).astype(np.uint8)
    return np.stack((bitArray, bitArray, bitArray), axis=2) * 255


def toOneBit(image: rgb) -> rgb:
    flat_array = np.round((np.mean(image, axis=2)))
    cutoff = np.mean(flat_array)
    bitArray = (flat_array >= cutoff).astype(np.uint8)
    return np.stack((bitArray, bitArray, bitArray), axis=2) * 255


## Tiling ##

def tilesByRow(image: rgb, shape: Tuple[int, int] = (100, 100)) -> list[rgb]:
    h0, w0 = image.shape[:2]
    h1, w1 = shape
    y, x = 0, 0
    rows = []
    while y + h1 <= h0:
        row = []
        while x + w1 <= w0:
            row.append(image[y: y+h1, x: x+w1, :])
            x += w1
        x = 0
        y += h1
        rows.append(row)
    return rows


## Effects ##


def addBorder(image: rgb, width: int, color: color = np.array([0, 0, 0])) -> rgb:
    padded = np.pad(image, ((width, width), (width, width), (0, 0)), mode='constant',
                    constant_values=((0, 0), (0, 0), (0, 0)))

    borderMult = np.zeros((padded.shape[0], padded.shape[1], 1))
    borderMult[:width, :] = 1
    borderMult[:, :width] = 1
    borderMult[-width:, :] = 1
    borderMult[:, -width:] = 1

    border = np.kron(borderMult, color)

    return padded + border


def addRgbNoise(image: rgb, sigma: int = 60) -> rgb:
    noise = np.rint(sigma * rng.standard_normal(image.shape))
    return np.clip(image + noise, 0, 255).astype(np.uint8)


def multContrast(image: rgb, mult: float = 2) -> rgb:
    avg = np.median(image)
    normed = image.astype(int) - avg
    return np.clip(normed * mult + avg, 0, 255).astype(np.uint8)


def multContrastMean(image: rgb, mult: float = 2) -> rgb:
    avg = np.mean(image)
    normed = image.astype(int) - avg
    return np.clip(normed * mult + avg, 0, 255).astype(np.uint8)
