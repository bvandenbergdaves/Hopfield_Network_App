import numpy as np

## Global Variables ##
upScale = 10

onColor = np.array((0, 0, 0))
offColor = np.array((255, 255, 255))

turnOnColor = np.array((0, 0, 255))
turnOffColor = np.array((255, 0, 0))

black = np.array((0, 0, 0))
white = np.array((255, 255, 255))


def makePixel(scale: int, color: np.array) -> np.array:
    return np.kron(np.ones((scale, scale, 1)), color)


def addBorder(pixel: np.array, color: np.array) -> np.array:
    newPixel = pixel.copy()
    for i in [0, -1]:
        for c in range(3):
            newPixel[i, :, c] = color[c]
            newPixel[:, i, c] = color[c]
    return newPixel


def bitsToRgb(bits: np.array, shape: tuple[int], border: bool = True) -> np.array:
    px0 = makePixel(upScale, offColor)
    px1 = makePixel(upScale, onColor)
    if border:
        px0 = addBorder(px0, black)
        px1 = addBorder(px1, black)

    bits = np.reshape(bits, (shape[0], shape[1], 1))
    result = np.kron((bits + 1) % 2, px0) + np.kron(bits, px1)
    return np.round(result).astype(np.uint8)


def probsToRgb(probs: np.array, shape: tuple[int], border: bool = True) -> np.array:
    px0 = makePixel(upScale, turnOffColor)
    px1 = makePixel(upScale, turnOnColor)
    if border:
        px0 = addBorder(px0, black)
        px1 = addBorder(px1, black)

    probs = np.reshape(probs, (shape[0], shape[1], 1))
    result = np.kron((1-probs), px0) + np.kron(probs, px1)
    return np.round(result).astype(np.uint8)


def heatMap(bits: np.array, probs: np.array, shape: tuple[int], border: bool = True) -> np.array:
    image = bitsToRgb(bits, shape, border)
    colors = probsToRgb(probs, shape, border)
    return np.concatenate((image, colors), axis=1).astype(np.uint8)
