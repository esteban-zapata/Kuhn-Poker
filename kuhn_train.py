import random, pickle, time
from typing import *
from nodes import kNode
from test import Test
import numpy as np
from multiprocessing import Pool, cpu_count

NUM_ACTIONS = 2

nodeMap = {}

def continueTrain(file, iterations: int, saveName):
    kuhntest = Test()
    kuhntest.read(file)
    global nodeMap
    nodeMap = kuhntest.nodeMap
    train(iterations, saveName)


def continueTrainPrune(file, iterations: int, saveName):
    kuhntest = Test()
    kuhntest.read(file)
    global nodeMap
    nodeMap = kuhntest.nodeMap
    trainPrune(iterations, saveName)


def train(iterations: int, saveName):
    t1 = time.time()
    cards = np.array([1, 2, 3])
    util = 0
    batch_size = 1000
    for i in range(1, iterations, batch_size):
        batch_util = 0
        for _ in range(batch_size):
            np.random.shuffle(cards)
            batch_util += cfr(cards, '', 1, 1)
        util += batch_util

        if i % (100000) == 0:
            if time.time() - t1 != 0.:
                print(f"Kuhn trained {i} iterations. {str(100000 / (time.time() - t1))} iterations per second")
            my = Test()
            my.nodeMap = nodeMap
            print("Average game value: " + str(my.gameValue()))
            print(f"Worst case game value: {my.exploitability()}")
            print(f"Total exploitability: {-sum(my.exploitability())}")
            t1 = time.time()

    my = Test()
    my.nodeMap = nodeMap
    print("Strategy: ")
    for node in nodeMap.values():
        print(node)
    print("Average game value: " + str(my.gameValue()))

    with open(saveName, 'wb') as f:
        pickle.dump(nodeMap, f)


def trainPrune(iterations: int, savePath):
    t1 = time.time()
    cards = np.array([1, 2, 3])
    util = 0
    batch_size = 1000
    for i in range(1, iterations, batch_size):
        batch_util = 0
        for _ in range(batch_size):
            np.random.shuffle(cards)
            batch_util += cfrPrune(cards, '', 1, 1)
        util += batch_util

        if i % (100000) == 0:
            my = Test()
            my.nodeMap = nodeMap
            print(f"Kuhn trained {i} iterations. {str(100000 / (time.time() - t1))} iterations per second.")
            print(f"Total exploitability: {sum(my.exploitability())}")
            t1 = time.time()

    my = Test()
    my.nodeMap = nodeMap

    for node in nodeMap.values():
        print(node)
    print("Average game value: " + my.gameValue())

    with open(savePath, 'wb') as f:
        pickle.dump(nodeMap, f)


def cfr(cards: np.ndarray, history: str, p0: float, p1: float) -> float:
    plays = len(history)
    curr_player = plays % 2

    infoSet = str(cards[curr_player]) + history

    curr_node = kNode()
    curr_node.children = infoSet
    payoff = curr_node.returnPayoff(cards)
    terminalNode = payoff is not None

    if terminalNode:
        return payoff

    curr_node = nodeMap.get(infoSet)
    if curr_node is None:
        curr_node = kNode()
        curr_node.children = infoSet
        nodeMap[infoSet] = curr_node

    realization_weight = p1 if curr_player == 0 else p0
    strategy = curr_node.getStrategy(realization_weight)
    util = np.zeros(NUM_ACTIONS)

    nodeUtil = 0
    for a in range(NUM_ACTIONS):
        nextHistory = history + ('p' if a == 0 else 'b')
        if curr_player == 0:
            util[a] = -cfr(cards, nextHistory, p0 * strategy[a], p1)
        else:
            util[a] = -cfr(cards, nextHistory, p0, p1 * strategy[a])
        nodeUtil += strategy[a] * util[a]

    for a in range(NUM_ACTIONS):
        regret = util[a] - nodeUtil
        curr_node.regretSum[a] += (p1 if curr_player == 0 else p0) * regret
    return nodeUtil


def cfrPrune(cards: np.ndarray, history: str, p0: float, p1: float) -> float:
    plays = len(history)
    curr_player = plays % 2

    infoSet = str(cards[curr_player]) + history

    curr_node = kNode()
    curr_node.children = infoSet
    payoff = curr_node.returnPayoff(cards)
    terminalNode = payoff is not None

    if terminalNode:
        return payoff

    curr_node = nodeMap.get(infoSet)
    if curr_node is None:
        curr_node = kNode()
        curr_node.children = infoSet
        nodeMap[infoSet] = curr_node

    realization_weight = p1 if curr_player == 0 else p0
    strategy = curr_node.getStrategy(realization_weight)
    util = np.zeros(NUM_ACTIONS)

    nodeUtil = 0
    for a in curr_node.promising_branches:
        nextHistory = history + ('p' if a == 0 else 'b')
        if curr_player == 0:
            util[a] = -cfr(cards, nextHistory, p0 * strategy[a], p1)
        else:
            util[a] = -cfr(cards, nextHistory, p0, p1 * strategy[a])
        nodeUtil += strategy[a] * util[a]

    for a in curr_node.promising_branches:
        regret = util[a] - nodeUtil
        curr_node.regretSum[a] += (p1 if curr_player == 0 else p0) * regret
    return nodeUtil


if __name__ == '__main__':
    start_time = time.time()
    train(10 ** 6, "kt-10")
    print("--- %s seconds ---" % (time.time() - start_time))
