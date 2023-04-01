import numpy as np


def hammingDist(bits0: np.array, bits1: np.array) -> float:
    return np.sum(np.abs(bits0 - bits1)) / bits0.size


def findSiblings(patterns: list[np.array], idx: int, cutoff: float = 0.4) -> set[int]:
    siblings = set()
    for i, pattern in enumerate(patterns):
        dist = hammingDist(pattern, patterns[idx])
        if dist <= cutoff or 1 - cutoff <= dist:
            siblings.add(i)
    return siblings


def findSiblingDict(patterns: list[np.array], idx: int, cutoff: float = 0.4) -> dict[int, set[int]]:
    siblingDict = dict()
    for i in range(len(patterns)):
        siblingDict[i] = findSiblings(patterns, i, cutoff)
    return siblingDict


def filterSiblings(patterns: list[np.array], cutoff: float = 0.4) -> list[int]:
    siblingDict = findSiblingDict(patterns, cutoff)
    for i in range(len(patterns)):
        siblingDict[i] = findSiblings(patterns, i, cutoff)
    siblingList = [{'set': siblingDict[i], 'idx': i}
                   for i in range(len(patterns)) if len(siblingDict[i]) > 1]
    onlyChildren = [{'set': siblingDict[i], 'idx': i}
                    for i in range(len(patterns)) if len(siblingDict[i]) == 1]

    while True:
        if len(siblingList) == 0:
            break
        siblingList.sort(key=lambda dct: len(dct['set']), reverse=True)
        siblings, idx = siblingList[0].values()
        if len(siblings) > 1:
            siblingList.pop(0)
            siblings.remove(idx)
            for i in siblings:
                siblingDict[i].remove(idx)
        else:
            break
    siblingList.extend(onlyChildren)
    return [patterns[dct['idx']] for dct in siblingList]
