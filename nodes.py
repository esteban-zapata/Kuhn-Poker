import random
from typing import List, Dict, Optional

Pass = 0
Bet = 1
Num_Actions = 2
rand = random.Random()


class Node():
    def __init__(self):
        self.children = ''
        self.strategy = [0.0] * Num_Actions
        self.regretSum = [0.0] * Num_Actions
        self.strategySum = [0.0] * Num_Actions

    def __str__(self):
        return self.children + '' + ', '.join(str(x) for x in self.getAvgStrat())

    def getStrategy(self, realization_weight: float):
        normalizeSum = 0
        for a in range(Num_Actions):
            self.strategy[a] = self.regretSum[a] if self.regretSum[a] > 0 else 0
            normalizeSum += self.strategy[a]
        for a in range(Num_Actions):
            self.strategy[a] = self.strategy[a] / normalizeSum if normalizeSum > 0 else 1.0 / Num_Actions
            self.strategySum[a] += realization_weight * self.strategy[a]
        return self.strategy

    def getAvgStrat(self) -> List[float]:
        avgStrat = [0.0] * Num_Actions
        normalizeSum = 0
        for a in range(Num_Actions):
            normalizeSum += self.strategySum[a]
        for a in range(Num_Actions):
            avgStrat[a] = self.strategySum[a] / normalizeSum if normalizeSum > 0 else 1.0 / Num_Actions
        return avgStrat

    def returnPayoff(self, cards: List[int]) -> Optional[int]:
        history = self.children[1:len(self.children)]
        plays = len(history)
        currentPlayer = plays % 2
        opp = 1 - currentPlayer

        if plays > 1:
            terminalPass = history[plays - 1] == 'p'
            doubleBet = history[plays - 2] == 'bb'
            isPlayerCardHigher = cards[currentPlayer] > cards[opp]
            if terminalPass:
                if history == 'pp':
                    return 1 if isPlayerCardHigher else -1
                else:
                    return 1
            elif doubleBet:
                return 2 if isPlayerCardHigher else -2
