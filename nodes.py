import random
from typing import List, Dict

Pass = 0
Bet = 1
Num_Actions = 2
rand = random.Random()


class Node():
    def __init__(self):
        self.children = {}
        self.strategy = [0.0] * Num_Actions
        self.regretSum = [0.0] * Num_Actions
        self.strategySum = [0.0] * Num_Actions

    def __str__(self):
        return f"Strategy: {self.strategy}, Regret: {self.regretSum}, StrategySum: {self.strategySum}"

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
