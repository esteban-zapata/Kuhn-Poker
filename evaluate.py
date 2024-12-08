import pickle
import numpy as np
from nodes import kNode

def load_strategy(file):
    with open(file, 'rb') as f:
        nodeMap = pickle.load(f)
    return nodeMap

def simulate_game(nodeMap):
    cards = np.array([1, 2, 3])
    np.random.shuffle(cards)
    history = ''
    p0, p1 = 1, 1
    plays = 0
    while True:
        curr_player = plays % 2
        infoSet = str(cards[curr_player]) + history
        node = nodeMap.get(infoSet)
        if node is None:
            node = kNode()
            node.children = infoSet
            nodeMap[infoSet] = node
        strategy = node.getStrategy(1)
        action = np.random.choice([0, 1], p=strategy)
        history += 'p' if action == 0 else 'b'
        payoff = node.returnPayoff(cards)
        if payoff is not None:
            return payoff
        plays += 1

def simulate_games(nodeMap, num_games):
    total_reward = 0
    wins = 0
    for _ in range(num_games):
        reward = simulate_game(nodeMap)
        total_reward += reward
        if reward > 0:
            wins += 1
    win_rate = wins / num_games
    print(f'Total rewards: {total_reward}')
    print(f'Number of games: {num_games}')
    avg_reward = total_reward / num_games
    return win_rate, avg_reward

def calculate_exploitability(nodeMap):
    exploitability = 0
    cards = np.array([1, 2, 3])
    cardList = [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]
    for cards in cardList:
        for i in range(2):
            infoSet = str(cards[i])
            strategy = nodeMap.get(infoSet).getAvgStrat()
            for a in range(2):
                exploitability += strategy[a] * abs(strategy[a] - 0.5)
    return exploitability



if __name__ == '__main__':
    # Load the trained strategy
    nodeMap = load_strategy("kt-64M")

    # Simulate games to calculate win rate and average reward
    num_games = 10000
    win_rate, avg_reward = simulate_games(nodeMap, num_games)
    print(f"Win Rate: {win_rate}")
    print(f"Average Reward: {avg_reward}")

    # Calculate exploitability
    exploitability = calculate_exploitability(nodeMap)
    print(f"Exploitability: {exploitability}")
