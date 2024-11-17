## ML Project
## Esteban Zapata & Raxel Ortiz
import numpy as np
from node import Node  # Import the Node class from node.py
from model import create_model  # Import the create_model function from model.py

class KuhnTrainer:
    def __init__(self):
        self.cards = [1, 2, 3]
        self.num_actions = 2  # Two actions: pass (p) and bet (b)
        self.node_map = {}
        self.model = create_model((2,))  # Create a neural network model

    def get_node(self, history):
        if history not in self.node_map:
            self.node_map[history] = Node(history, self.model)
        return self.node_map[history]

    def cfr(self, history, p0, p1):
        plays = len(history)
        player = plays % 2
        opponent = 1 - player

        # Check for terminal states
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

        # Get the node for the current history
        node = self.get_node(history)
        strategy = node.get_strategy(p0 if player == 0 else p1)
        util = np.zeros(self.num_actions)
        node_util = 0

        # Update cumulative regrets
        for a in range(self.num_actions):
            next_history = history + ('p' if a == 0 else 'b')
            if player == 0:
                util[a] = -self.cfr(next_history, p0 * strategy[a], p1)
            else:
                util[a] = -self.cfr(next_history, p0, p1 * strategy[a])
            node_util += strategy[a] * util[a]

        # for a in range(self.num_actions):
        #     regret = util[a] - node_util
        #     if player == 0:
        #         node.regret_sum[a] += p1 * regret
        #     else:
        #         node.regret_sum[a] += p0 * regret

        return node_util

    def train(self, iterations):
        util = 0
        for i in range(iterations):
            np.random.shuffle(self.cards)
            util += self.cfr("", 1, 1)
        print(f"Average game value: {util / iterations}")

    def get_final_strategy(self):
        return {k: node.get_average_strategy() for k, node in self.node_map.items()}

if __name__ == "__main__":
    trainer = KuhnTrainer()
    trainer.train(10000)
    final_strategy = trainer.get_final_strategy()
    print("Final Strategy:")
    for history, strategy in final_strategy.items():
        print(f"History: {history}, Strategy: {strategy}")
