from typing import Dict
import pickle
import random


class KuhnPoker():
    AI: Dict

    def read(self, filepath: str):
        with open(filepath, 'rb') as f:
            self.AI = pickle.load(f)

    def playAI(self, first: bool, bank: int):
        cards = [1, 2, 3]
        random.shuffle(cards)
        print("you have: $" + str(bank))
        print("====================================\n")
        if first: print("Your card is: " + str(cards[0]))
        else: print("Your card is: " + str(cards[1]))
        self.playAI(first, bank + self.recursive(cards, '', first))

    def recursive(self, cards, history: str, first: bool):
        players = ["User", "AI"]
        plays = len(history)
        AI_Turn = (plays % 2 == 1) if first else plays % 2 == 0
        current_player = plays % 2
        opponent = 1 - current_player
        AI_cards = str(cards[1]) if first else str(cards[0])
        if plays > 1:
            terminalPass = history[plays - 1] == 'p'
            doubleBet = history[plays - 2: plays] == 'bb'
            isPlayerCardHigher = cards[current_player] > cards[opponent]
            if terminalPass:
                if history == 'pp':
                    if isPlayerCardHigher:
                        print("AI had " + AI_cards + ". History: " + history + ".\n" +
                             (players[1] if AI_Turn else players[0]) + " won $1.")
                        return -1 if AI_Turn else 1
                    else:
                        print("AI had " + AI_cards + ". History: " + history + ".\n" +
                             (players[0] if AI_Turn else players[1]) + " won $1.")
                        return 1 if AI_Turn else -1
                else:
                    print("AI had " + AI_cards + ". History: " + history + ".\n" +
                         (players[1] if AI_Turn else players[1]) + " won $1.")
                    return -1 if AI_Turn else 1
            elif doubleBet:
                if isPlayerCardHigher:
                    print("AI had " + AI_cards + ". History: " + history + ".\n" +
                         (players[1] if AI_Turn else players[0]) + " won $2.")
                    return -2 if AI_Turn else 2
                else:
                    print("AI had " + AI_cards + ". History: " + history + ".\n" +
                         (players[0] if AI_Turn else players[1]) + " won $2.")
                    return 2 if AI_Turn else -2
        infoSet = str(cards[current_player]) + history
        if AI_Turn:
            AI_Strat = self.AI[infoSet].getAvgStrat()
            rand = random.random()
            # if AI decideds to passes
            if rand < AI_Strat[0]:
                print("AI passed.\n")
                return self.recursive(cards, history + 'p', first)
            else:
                print("AI bets $1.\n")
                return self.recursive(cards, history + 'b', first)
        else:
            userInput = input("Do you want to bet or pass? (b/p): ")
            if userInput == 'p':
                print("You passed.\n")
                return self.recursive(cards, history + 'p', first)
            elif userInput == 'b':
                print("You bet $1.\n")
                return self.recursive(cards, history + 'b', first)
            else:
                return self.recursive(cards, history, first)


if __name__ == '__main__':
    game = KuhnPoker()
    game.read('kt-100M')
    game.playAI(False, 0)
