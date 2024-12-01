import random
from typing import List, Optional

PASS = 0
BET = 1
NUM_ACTIONS = 2
rand = random.random()


class kNode():
    def __init__(self):
        self.children = ''
        self.strategy = [0] * NUM_ACTIONS
        self.regretSum = [0] * NUM_ACTIONS
        self.strategySum = [0] * NUM_ACTIONS

    def __str__(self):
        return self.children + '' + ', '.join(str(x) for x in self.getAvgStrat())

    def getStrategy(self, realization_weight: float) -> List[float]:
        normalizeSum = 0
        for a in range(NUM_ACTIONS):
            if self.regretSum[a] > 0:
                self.strategy[a] = self.regretSum[a]
            else:
                self.strategy[a] = 0
            normalizeSum += self.strategy[a]
        for a in range(NUM_ACTIONS):
            if normalizeSum > 0:
                self.strategy[a] /= normalizeSum
            else:
                self.strategy[a] = 1 / NUM_ACTIONS
            self.strategySum[a] += realization_weight * self.strategy[a]
        return self.strategy

    def getAvgStrat(self) -> list:
        avgStrat = [0] * NUM_ACTIONS
        normalizeSum = sum(self.strategySum)
        for a in range(NUM_ACTIONS):
            if normalizeSum > 0:
                avgStrat[a] = self.strategySum[a] / normalizeSum
            else:
                avgStrat[a] = 1.0 / NUM_ACTIONS
        for a in range(NUM_ACTIONS):
            if avgStrat[a] < 0.01:
                avgStrat[a] = 0
        normalizeSum = sum(avgStrat)
        for a in range(NUM_ACTIONS):
            avgStrat[a] /= normalizeSum
        return avgStrat

    def returnPayoff(self, cards: List[int]) -> Optional[int]:
        history = self.children[1:len(self.children)]
        plays = len(history)
        currentPlayer = plays % 2
        opp = 1 - currentPlayer

        if plays > 1:
            terminalPass = history[plays - 1] == 'p'
            doubleBet = history[plays - 2: plays] == 'bb'
            isPlayerCardHigher = cards[currentPlayer] > cards[opp]
            if terminalPass:
                if history == 'pp':
                    if isPlayerCardHigher:
                        return 1
                    else:
                        return -1
                else:
                    return 1
            elif doubleBet:
                if isPlayerCardHigher:
                    return 2
                else:
                    return -2
