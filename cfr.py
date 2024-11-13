## ML Project 
## Esteban Zapata & Raxel Ortiz
import numpy as np

class KuhnTrainer:
    def __init__(self):
        #Defing the cards and number of actions (pass, bet)
        # J, K, Q = 1, 2, 3
        self.cards = [1, 2, 3]
        self.num_actions = 2 # Two actions: pass (p) and bet (b)
        #initialize dictionaries to store cumulative regrets and strats, and strat sums
        self.cumulative_regrets = {}
        self.strategy = {}
        self.strategy_sum = {}
        self.opponent_strategy = {}

    def get_information_set_key(self, history):
        #use history as the key for the information set
        return history

    def get_strategy(self, history):
        # If the history is no in strat dict, initialize it
        if history not in self.strategy:
            self.strategy[history] = np.ones(self.num_actions) / self.num_actions
            self.cumulative_regrets[history] = np.zeros(self.num_actions)
            self.strategy_sum[history] = np.zeros(self.num_actions)

        # Compute the current strat from the cumulative regrets
        regret_sum = np.sum(self.cumulative_regrets[history])
        strategy = np.maximum(self.cumulative_regrets[history], 0)
        if regret_sum > 0:
            strategy /= regret_sum
        else:
            strategy = np.ones(self.num_actions) / self.num_actions

        #Update strat sum and return current strategy
        self.strategy[history] = strategy
        self.strategy_sum[history] += strategy
        ## print(f"History: {history}, Strategy: {self.strategy[history]}, Cumulative Regrets: {self.cumulative_regrets[history]}")

        return strategy

    def get_average_strategy(self, history):
        #compute the average strategy over all the training iterations
        normalizing_sum = np.sum(self.strategy_sum[history])
        if normalizing_sum > 0:
            return self.strategy_sum[history] / normalizing_sum
        else:
            return np.ones(self.num_actions) / self.num_actions

    def cfr(self, history, p0, p1):
        plays = len(history)
        player = plays % 2
        opponent = 1 - player

        # to check for terminal states
        if plays > 1:
            terminal_pass = history[-1] == 'p'
            double_bet = history[-2:] == 'bb'
            is_player_card_higher = self.cards[player] > self.cards[opponent]
            if terminal_pass:
                if history == "pp":
                    return 1 if is_player_card_higher else -1
                else:
                    return 1
            elif double_bet:
                return 2 if is_player_card_higher else -2

        # Recursively compute the utility of each section
        strategy = self.get_strategy(history)
        util = np.zeros(self.num_actions)
        node_util = 0

        # update cumulative regrets
        for a in range(self.num_actions):
            next_history = history + ('p' if a == 0 else 'b')
            if player == 0:
                util[a] = -self.cfr(next_history, p0 * strategy[a], p1)
            else:
                util[a] = -self.cfr(next_history, p0, p1 * strategy[a])
            node_util += strategy[a] * util[a]

        for a in range(self.num_actions):
            regret = util[a] - node_util
            if player == 0:
                self.cumulative_regrets[history][a] += p1 * regret
            else:
                self.cumulative_regrets[history][a] += p0 * regret

        return node_util
  
    def train(self, iterations):
        util = 0
        # shuffle cards and run the CFR
        for i in range(iterations):
            np.random.shuffle(self.cards)
            util += self.cfr("", 1, 1)
        print(f"Average game value: {util / iterations}")

    def get_final_strategy(self):
        return {k: self.get_average_strategy(k) for k in self.strategy.keys()}



if __name__ == "__main__":
    trainer = KuhnTrainer()
    trainer.train(10) 
    final_strategy = trainer.get_final_strategy()
    print("Final Strat!:")
    for history, strategy in final_strategy.items():
        print(f"History: {history}, strategy: {strategy}")