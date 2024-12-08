# Kuhn Poker
Esteban Zapata and Raxel Ortiz
## Rules:
  - 2 players
  - 3 card deck {A, K, Q}
  - Each starts the hand with $2
  - Each antes (i.e., makes forced bet of) $1 at the start of the hand
  - Each player is dealt 1 card
  - Each has $1 remaining for betting
  - There is 1 betting round and 1 bet size of $1
  - The highest card is the best (i.e., A > K > Q)

~Action starts with P1, who can Bet $1 or Check

If P1 bets, P2 can either Call or Fold
If P1 checks, P2 can either Bet or Check
If P2 bets after P1 checks, P1 can then Call or Fold
These outcomes are possible:

If a player folds to a bet, the other player wins the pot of $2 (profit of $1)
If both players check, the highest card player wins the pot of $2 (profit of $1)
If there is a bet and call, the highest card player wins the pot of $4 (profit of $2)

## How to play:
Run the game by executing the following command in the terminal:
```python
python kuhn_poker.py
```
## How to train the AI:
Run the training script by executing the following command in the terminal:
```python
python kuhn_train.py
```
## See the Metrics:
Run the metrics script by executing the following command in the terminal:
```python
python test.py evaluate.py
```
