import numpy as np
import Model.functions.rgbArrays as rgb
## Conversion Func ##


def rgbToBits(rgb_array: np.array) -> np.array:
    oneBit = rgb.toOneBit(rgb_array)
    reds = np.clip(oneBit[:, :, 0], 0, 1)
    return reds.flatten(order='C').astype(int)
