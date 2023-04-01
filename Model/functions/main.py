import pickle
import os
import numpy as np
from Model.functions.hopfield import DiscreteHopfield
from Model.functions.imToRgb import getImageTiles, getImages, getImageNames
from Model.functions.RgbToBits import rgbToBits
from Model.functions.patternFiltering import filterSiblings
from Model.functions.bitsToRgb import heatMap, bitsToRgb
from Model.functions.RgbToIm import saveImage, saveGif
from Model.functions.rgbArrays import compress, multContrast, toOneBitMedian


## Image Prep ##
def getImageDict(path: str) -> dict[str, np.array]:
    names = getImageNames(path)
    rgb_arrays = getImages(path)
    return dict(zip(names, rgb_arrays))


def compressImages(path0='_images/imported', path1='_images/_edit0'):
    names = getImageNames(path0)
    rgb_arrays = getImages(path0)
    compRates = []
    for im in rgb_arrays:
        if im.size >= 1280 * 720:
            compRates.append(5)
        elif im.size >= 640 * 480:
            compRates.append(3)
        elif im.size >= 200 * 200:
            compRates.append(2)
        else:
            compRates.append(1)

    compressed = map(compress, rgb_arrays, compRates)
    for im, name in zip(compressed, names):
        saveImage(im, name + 'contrast', path1)


def multContrastImages(path0='_images/imported', path1='_images/_edit1'):
    names = getImageNames(path0)
    rgb_arrays = getImages(path0)
    mults = []
    for im in rgb_arrays:
        mults.append(1.5)

    processed = map(multContrast, rgb_arrays, mults)
    for im, name in zip(processed, names):
        saveImage(im, name + 'contrast', path1)


def convertToOneBitImages(path0, path1='_images/_oneBits'):
    names = getImageNames(path0)
    rgb_arrays = getImages(path0)

    processed = map(toOneBitMedian, rgb_arrays)
    for im, name in zip(processed, names):
        saveImage(im, name, path1)


## Patterns ##
def generatePatterns(path: str, shape: tuple[int], cutoff: float = 0.4) -> np.array:
    rgb_arrays = getImageTiles(path, shape)
    bit_arrays = list(map(rgbToBits, rgb_arrays))
    return np.stack(filterSiblings(bit_arrays, cutoff))


## Network ##
def loadNetwork(name: str, path: str = '') -> DiscreteHopfield:
    start = os.getcwd()
    os.chdir(f'{start}/{path}/{name}')
    weights = np.load('weights.npy')
    patterns = np.load('patterns.npy')
    with open('info.pickle', 'rb') as file:
        info = pickle.load(file)
    temp = info['temp']
    density = info['density']
    shape = info['shape']
    os.chdir(start)

    network = DiscreteHopfield(shape)
    network.setTemp(temp)
    network.setWeights(weights, density)
    network.setPatterns(patterns, shape)
    return network


def makeNetwork(patterns: np.array, density: float = 1, shape: tuple[int] = None) -> DiscreteHopfield:
    if shape is None:
        shape = patterns.shape[1]
    network = DiscreteHopfield(shape)
    network.hebbTrain(patterns, density)
    return network


def saveNetwork(network: DiscreteHopfield, name: str, path: str = '') -> None:
    start = os.getcwd()
    os.chdir(f'{start}/{path}')
    os.mkdir(name)
    os.chdir(name)
    np.save('weights.npy', network.weights)
    np.save('patterns.npy', network.patterns)
    with open('info.pickle', 'wb') as file:
        pickle.dump(network.info, file, protocol=pickle.HIGHEST_PROTOCOL)
    if network.info['shape'] is not None:
        os.mkdir('patterns')
        for i, pattern in enumerate(network.patterns):
            rgb_array = bitsToRgb(pattern, network.info['shape'])
            saveImage(rgb_array, f'{i}.png', path='patterns')
    os.chdir(start)


def makeNetworkFromFolder(import_folder, save_folder, width, height, cutoff, density, name):
    print('Creating network. This may take a while.')
    patterns = generatePatterns(import_folder, (height, width), cutoff)
    print(f'generated {len(patterns)} patterns')
    network = makeNetwork(patterns, density, (height, width))
    print('trained network')
    saveNetwork(network, name, save_folder)
    print('saved network')



## Evolution ##
def initializeState(network: DiscreteHopfield, idx: int, temp: float, noise: float):
    network.setTemp(temp)
    network.setToPattern(idx)
    network.addNoise(noise)


def runNetwork(network: DiscreteHopfield, n: int, sampleRate: int) -> tuple[list[np.array]]:
    states = [network.getState()]
    probs = [network.onesProb()]
    for _ in range(n // sampleRate):
        network.iterate(n=sampleRate)
        states.append(network.getState())
        probs.append(network.onesProb())
    return states, probs


def runNetworkSync(network: DiscreteHopfield, n: int) -> tuple[list[np.array]]:
    states = [network.getState()]
    probs = [network.onesProb()]
    for _ in range(n):
        network.iterateSync()
        states.append(network.getState())
        probs.append(network.onesProb())
    return states, probs


## Rendering ##
def render(states: list[np.array], probs: list[np.array], shape: tuple[int]) -> np.array:
    frames = list(map(heatMap, states, probs, [shape]*len(states)))
    return np.stack(frames)


def makeNetworkAnimation(import_folder, save_folder, network_name, pattern_number,
                             tempurature, noise, number_of_iterations, sample_rate, fps):
        network = loadNetwork(network_name, import_folder)
        network.setTemp(tempurature)
        network.setToPattern(pattern_number)
        network.addNoise(noise)
        states, probs = runNetwork(network, number_of_iterations, sample_rate)
        print(f'pattern {pattern_number} run')

        frames = render(states, probs, network.info['shape'])
        saveGif(frames, network_name + f'_{pattern_number}', path=save_folder, fps=fps)
        print(f'gif {pattern_number} rendered and saved')
