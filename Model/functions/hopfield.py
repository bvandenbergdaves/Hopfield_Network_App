import numpy as np

## Ising Arrays ##

rng = np.random.default_rng()


def isingToBits(ising: np.array) -> np.array:
    return np.clip(ising + 1, 0, 1)


def bitsToIsing(bits: np.array) -> np.array:
    return bits - (bits + 1) % 2


def addNoise(ising: np.array, flipChance: float) -> np.array:
    ising = ising.copy()
    flips = rng.random(size=ising.size) < flipChance
    for i in range(ising.size):
        if flips[i]:
            ising[i] *= -1
    return ising


def randomIsing(size: int) -> np.array:
    bits = rng.integers(2, size=size)
    return bitsToIsing(bits)




class DiscreteHopfield:
    def __init__(self, shape: int or tuple(int)):
        # immutable
        self.size = shape if isinstance(shape, int) else shape[0] * shape[1]

        # mutable
        self.info = {'temp': 0, 'density': None,
                     'shape': None if isinstance(shape, int) else shape}

        self.probFunc = lambda x: np.heaviside(x, 1)
        self.state = None
        self.patterns = None
        self.weights = None

    def activation(self) -> np.array:
        return self.weights @ self.state

    def onesProb(self) -> np.array:
        return self.probFunc(self.activation())

    @property
    def stayChances(self) -> np.array:
        return np.abs(self.onesProb() + np.clip(self.state, -1, 0))

    def stability(self) -> float:
        return np.mean(self.stayChances)[0]

    ## Temp ##
    def setTemp(self, temp: float) -> None:
        self.info['temp'] = temp
        if temp == 0:
            self.probFunc = lambda x: np.heaviside(x, 1)
        else:
            self.probFunc = lambda x: 1 / (1 + np.exp(-2*x/temp))

    ## Weights and Density ##
    def setWeights(self, weights: np.array, density: int = None) -> None:
        self.info['density'] = density
        self.weights = weights

    ## Patterns and Shape ##
    def setPatterns(self, patterns: np.array, shape: tuple[int] = None) -> None:
        self.info['shape'] = shape
        self.patterns = patterns

    def hebbTrainDense(self, patterns: np.array) -> None:
        self.info['density'] = 1
        self.weights = np.zeros((self.size, self.size))
        self.patterns = patterns
        isingPatterns = bitsToIsing(patterns)

        for i in range(self.size):
            j = i+1
            while j < self.size:
                w = (isingPatterns[:, i] @ isingPatterns[:, j]) / self.size
                self.weights[i, j] = w
                self.weights[j, i] = w
                j += 1

    def hebbTrain(self, patterns: np.array, density: float = 1) -> None:
        nPairs = int((self.size) * (self.size - 1) / 2)
        nSkips = round((1 - density) * nPairs)
        if nSkips == 0:
            self.hebbTrainDense(patterns)
        else:
            self.info['density'] = (nPairs - nSkips) / nSkips
            self.weights = np.zeros((self.size, self.size))
            self.patterns = patterns
            isingPatterns = bitsToIsing(patterns)

            pairs = np.arange(nPairs)
            skipIndices = rng.choice(pairs, size=nSkips, replace=False)
            bool_array = np.full(nPairs, True)
            for skip in skipIndices:
                bool_array[skip] = False

            i, j = 0, 1
            for instruction in bool_array:
                if instruction:
                    w = (isingPatterns[:, i] @ isingPatterns[:, j]) / self.size
                    self.weights[i, j] = w
                    self.weights[j, i] = w
                j += 1
                if j >= self.size:
                    i += 1
                    j = i+1

    ## State ##
    def getState(self) -> np.array:
        return isingToBits(self.state)

    def randomize(self) -> None:
        self.state = randomIsing(self.size)

    def setToPattern(self, idx: int) -> None:
        self.state = bitsToIsing(self.patterns[idx])

    def addNoise(self, flipChance) -> None:
        self.state = addNoise(self.state, flipChance)

    def iterate(self, n: int = 1) -> None:
        probs = self.stayChances
        for _ in range(n):
            idx = rng.integers(self.size)
            if rng.random() > probs[idx]:
                self.state[idx] *= -1
                probs = self.stayChances

    def iterateSync(self) -> None:
        probs = self.stayChances
        samples = rng.random(self.size)
        stayVec = (samples <= probs).astype(int)
        self.state *= bitsToIsing(stayVec)

    
