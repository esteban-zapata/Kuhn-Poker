# ML Project
# Esteban Zapata & Raxel Ortiz
import os
import numpy as np
import tensorflow as tf
from nodes import Node  # Import the Node class from node.py
from model import create_model  # Import the create_model function from model.py
from tensorflow.keras import layers, models
import random

class KuhnTrainer:
    def __init__(self, model_path):
        self.model_path = model_path
        input_shape = (2,)  # Example input shape with 2 features (player1_card, player2_card)
        if os.path.exists(self.model_path):
            print("Loading model...")
            self.model = tf.keras.models.load_model(self.model_path)
        else:
            print("Creating new model...")
            self.model = create_model(input_shape)

    def train(self, iterations=1000):
        # Example training logic
        print("Training the model...")
        game_history = []
        for _ in range(iterations):
            game_history.append(self.play_game())
        self.train_on_history(game_history)
        self.model.save(self.model_path)

    def play_game(self, use_model=False):
        # Example game simulation logic
        print("Playing a game of Kuhn Poker...")

        # Initialize deck and shuffle
        deck = [0, 1, 2]
        random.shuffle(deck)

        # Deal one card to each player
        player1_card = deck.pop()
        player2_card = deck.pop()

        # Initialize game state
        game_state = {
            'player1_card': player1_card,
            'player2_card': player2_card,
            'player1_action': None,
            'player2_action': None,
            'pot': 0
        }

        # Player 1's turn
        game_state['player1_action'] = self.get_action(player1_card, player2_card, use_model)
        if game_state['player1_action'] == 1:  # Player 1 bets
            game_state['pot'] += 1

        # Player 2's turn
        game_state['player2_action'] = self.get_action(player2_card, player1_card, use_model)
        if game_state['player2_action'] == 1:  # Player 2 bets
            game_state['pot'] += 1

        # Determine winner
        winner = self.determine_winner(game_state)
        game_state['winner'] = winner

        # Display game state
        self.display_game_state(game_state)

        return game_state

    def get_action(self, player_card, opponent_card, use_model):
        if use_model:
            # Use the trained model to predict the action
            features = np.array([[player_card, opponent_card]])
            prediction = self.model.predict(features)
            return 1 if prediction[0] > 0.5 else 0
        else:
            # Use a random action
            return random.choice([0, 1])

    def determine_winner(self, game_state):
        # Determine the winner based on the game state
        if game_state['player1_action'] == 0 and game_state['player2_action'] == 0:
            # Both players passed, highest card wins
            return 0 if game_state['player1_card'] > game_state['player2_card'] else 1
        elif game_state['player1_action'] == 1 and game_state['player2_action'] == 0:
            # Player 1 bet, Player 2 passed, Player 1 wins
            return 0
        elif game_state['player1_action'] == 0 and game_state['player2_action'] == 1:
            # Player 1 passed, Player 2 bet, Player 2 wins
            return 1
        else:
            # Both players bet, highest card wins
            return 0 if game_state['player1_card'] > game_state['player2_card'] else 1

    def train_on_history(self, game_history):
        # Convert game history to training data
        X = []
        y = []
        for game in game_history:
            # Example: Use player1_card and player2_card as features
            features = [game['player1_card'], game['player2_card']]
            # Example: Use winner as label
            label = game['winner']
            X.append(features)
            y.append(label)

        X = np.array(X)
        y = np.array(y)

        # Train the model
        self.model.fit(X, y, epochs=1000)

    def display_game_state(self, game_state):
        print(f"Player 1 card: {game_state['player1_card']}, Player 2 card: {game_state['player2_card']}")
        print(f"Player 1 action: {'bet' if game_state['player1_action'] == 1 else 'pass'}, Player 2 action: {'bet' if game_state['player2_action'] == 1 else 'pass'}")
        print(f"Pot: {game_state['pot']}")
        print(f"Winner: Player {game_state['winner'] + 1}")

def main():
    trainer = KuhnTrainer("path_to_your_model.h5")
    trainer.train(iterations=1000)
    trainer.play_game(use_model=True)

if __name__ == "__main__":
    main()
