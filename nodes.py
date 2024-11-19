import numpy as np
from model import create_model, encode_history

class Node:
    def __init__(self, info_set, model):
        self.info_set = info_set # Information set for node
        self.model = model
        self.strategy_sum = np.zeros(2) #sum of all strat so far

    def get_strategy(self, realization_weight):
        """ calculate the current mixed strat with regret matching """
        info_arr = encode_history(self.info_set).reshape(1, -1)
        strategy = self.model.predict(info_arr)[0]
        self.strategy_sum += realization_weight * strategy
        return strategy

    def get_average_strategy(self):
        """ get average strat across all iterations """
        normalizing_sum = np.sum(self.strategy_sum)
        if normalizing_sum > 0:
            return self.strategy_sum / normalizing_sum
        else:
            return np.ones(2) / 2 #uniform random strat

    def __str__(self):
        return f"InfoSet: {self.info_set}, AvgStrategy: {self.get_average_strategy()}"
