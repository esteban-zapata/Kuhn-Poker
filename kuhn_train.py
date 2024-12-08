import random, pickle, time
from typing import *
from nodes import kNode
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

    # Initialize promising_branches for each node
    for node in nodeMap.values():
        if not hasattr(node, 'promising_branches'):
            node.promising_branches = list(range(NUM_ACTIONS))

    trainPrune(iterations, saveName)


def train(iterations: int, saveName):
    t1 = time.time()
    # cards[0] as player 1
    # cards[1] as player 2
    cards = [1, 2, 3]
    util = 0
    for i in range(1, iterations):
        random.shuffle(cards)
        util += cfr(cards, '', 1, 1)

        freq_print = 100000
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
    # print("Average game value: " + my.gameValue())

    # Save trained algorithm
    with open(savePath, 'wb') as f:
        pickle.dump(nodeMap, f)

    # Prune branches based on regret values
    prune_threshold = 0.01
    for node in nodeMap.values():
        node.promising_branches = [a for a in range(NUM_ACTIONS) if node.regretSum[a] >= prune_threshold]


def cfr(cards: List[int], history: str, p0: float, p1: float) -> float:
    plays = len(history)
    curr_player = plays % 2

    infoSet = str(cards[curr_player]) + history

    curr_node = kNode()
    curr_node.children = infoSet
    payoff = curr_node.returnPayoff(cards)
    terminalNode = payoff is not None

    # Return payoff for terminal states
    if terminalNode:
        return payoff

    # Get information set node or create if nonexistent
    curr_node = nodeMap.get(infoSet)
    if curr_node is None:
        curr_node = kNode()
        curr_node.children = infoSet
        nodeMap[infoSet] = curr_node

    # For each action, recursively call cfr with additional history and probability
    realization_weight = p1 if curr_player == 0 else p0
    strategy = curr_node.getStrategy(realization_weight)
    util = [0] * NUM_ACTIONS

    # nodeUtil is the weighted average of the cfr of each branch,
    # weighted by the probability of traversing down a branch
    nodeUtil = 0
    for a in range(NUM_ACTIONS):
        nextHistory = history + ('p' if a == 0 else 'b')
        # The first probability is player 1's counterfactual probability
        if curr_player == 0:
            util[a] = -cfr(cards, nextHistory, p0 * strategy[a], p1)
        # Current player is 1
        else:
            util[a] = -cfr(cards, nextHistory, p0, p1 * strategy[a])
        nodeUtil += strategy[a] * util[a]

    # compute and accumulate cfr for each action
    for a in range(NUM_ACTIONS):
        regret = util[a] - nodeUtil
        curr_node.regretSum[a] += (p1 if curr_player == 0 else p0) * regret
    return nodeUtil


def cfrPrune(cards: List[int], history: str, p0: float, p1: float) -> float:
    plays = len(history)
    curr_player = plays % 2

    infoSet = str(cards[curr_player]) + history

    curr_node = kNode()
    curr_node.children = infoSet
    payoff = curr_node.returnPayoff(cards)
    terminalNode = payoff is not None

    # Return payoff for terminal states
    if terminalNode:
        return payoff

    # Get information set node or create it if nonexistent
    curr_node = nodeMap.get(infoSet)
    if curr_node is None:
        curr_node = kNode()
        curr_node.children = infoSet
        nodeMap[infoSet] = curr_node

    # For each action, recursively call cfr with additional history and probability
    realization_weight = p1 if curr_player == 0 else p0
    strategy = curr_node.getStrategy(realization_weight)
    util = [0] * NUM_ACTIONS

    # nodeUtil is the weighted average of the cfr of each branch,
    # weighted by the probability of traversing down a branch
    nodeUtil = 0
    for a in curr_node.promising_branches:
        nextHistory = history + ('p' if a == 0 else 'b')
        # The first probability is player 1's counterfactual probability
        if curr_player == 0:
            util[a] = -cfr(cards, nextHistory, p0 * strategy[a], p1)
        # Current player is 1
        else:
            util[a] = -cfr(cards, nextHistory, p0, p1 * strategy[a])
        nodeUtil += strategy[a] * util[a]

    # compute and accumulate cfr for each action
    for a in curr_node.promising_branches:
        regret = util[a] - nodeUtil
        curr_node.regretSum[a] += (p1 if curr_player == 0 else p0) * regret
    return nodeUtil


if __name__ == '__main__':
    import time
    start_time = time.time()
    continueTrainPrune('kt-10M', 10**7, 'kt-64M')
    print("--- %s seconds ---" % (time.time() - start_time))
