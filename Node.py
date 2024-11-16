import numpy as np
class Node:
    def __init__(self, info_set):
        self.info_set = info_set # Information set for node
        self.regret_sum = np.zeros(2)
        self.strategy = np.ones(2) / 2 #current strat for every action
        self.strategy_sum = np.zeros(2) #sum of all strat so far

    def get_strategy(self, realization_weight):
        """ calculate the current mixed strat with regret matching """
        normalizing_sum = np.sum(np.maximum(self.regret_sum, 0))
        if normalizing_sum > 0:
            self.strategy = np.maximum(self.regret_sum, 0) / normalizing_sum
        else:
            self.strategy = np.ones(2) / 2 #uniform random strat
        self.strategy_sum += realization_weight * self.strategy
        return self.strategy

    def get_average_strategy(self):
        """ get average strat across all iterations """
        normalizing_sum = np.sum(self.strategy_sum)
        if normalizing_sum > 0:
            return self.strategy_sum / normalizing_sum
        else:
            return np.ones(2) / 2 #uniform random strat

    def __str__(self):
        return f"InfoSet: {self.info_set}, AvgStrategy: {self.get_average_strategy()}"
