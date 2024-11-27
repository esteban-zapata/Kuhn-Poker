import random, pickle, time
from typing import *
from nodes import Node
from test import Test

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
    train(iterations, saveName)


def train(iterations: int, saveName):
    t1 = time.time()
    # cards[0] as player 1
    # cards[1] as player 2
    cards = [1, 2, 3]
    util = 0
    for i in range(1, iterations):
        random.shuffle(cards)
        util += cfr(cards, '', 1, 1)

        freq_print = 10000
        if i % (freq_print) == 0:
            if time.time() - t1 != 0.:
                print(f"Kuhn trained {i} iterations. {str(freq_print / (time.time() - t1))} iterations per second")
            my = Test()
            my.nodeMap = nodeMap
            print("Average game value: " + str(my.gameValue())) ##!!! Edit test.py to include gamevalue func.
            print(f"Worst case game value: {my.exploitability()}")
            print(f"Total exploitability: {-sum(my.exploitability())}")
            t1 = time.time()
        
        my = Test()
        my.nodeMap = nodeMap
        print("Strategy: ")
        for node in nodeMap.values():
            print(node)
        print("Aaverage game valuse: " + str(my.gameValue())) ##!!! Edit test.py to include gamevalue func.
        
        with open(saveName, 'wb') as f:
            pickle.dump(nodeMap, f)



def trainPrune(iterations: int, savePath):
    t1 = time.time()
    cards = [1, 2, 3]
    util = 0
    for i in range(1, iterations):
        random.shuffle(cards)
        util += cfrPrune(cards, '', 1, 1)
        
        # Progress
        if i % (10 ** 5) == 0:
            my = Test()
            my.nodeMap = nodeMap
            print(f"Kuhn trained {i} iterations. {str(10 ** 5 / (time.time() - t1))} iterations per second.")
            print(f"Total exploitability: {sum(my.exploitability())}")
            t1 = time.time()

    my = Test()
    my.nodeMap = nodeMap

    for node in nodeMap.values():
        print(node)
    print("Average game value: " + my.gameValue())

    # Save trained algorithm
    with open(savePath, 'wb') as f:
        pickle.dump(nodeMap, f)


def cfr():
    pass

def cfrPrune():
    pass



if __name__ == '__main__':
    import time
    start_time = time.time()
    train(10 ** 6, "kt-10")
    # continueTrain('kt-30Mp', 170*10**6, 'kt-200M')
    print("--- %s seconds ---" % (time.time() - start_time))