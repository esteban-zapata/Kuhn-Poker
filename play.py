import random

def play_game(human_card):
    ai_card = random.choice([card for card in [1, 2, 3] if card != human_card])

    # Human's turn
    human_action = input("Your turn: pass: (p) or bet: (b): ")
    while human_action not in ['p', 'b']:
        human_action = input("Invalid input. Please enter 'p' or 'b': ")

    # AI's turn
    if human_action == 'p':
        ai_action = 'p'
    else: 
        # AI's strategy (replace with model's strategy later)
        ai_action = 'b'  # For now assume the AI ALWAYS BETS after the human bets

        # TODO Feed info set to model

        #TODO Choose action with highest prob


    # Determine winner
    if human_action == 'b' and ai_action == 'b':
        if human_card > ai_card:
            print("You win!")
        else:
            print("AI wins!")
    else:
        print("It's a tie.")

if __name__ == "__main__":
    human_card = int(input("Enter your card (1, 2, or 3): "))
    while human_card not in [1, 2, 3]:
        human_card = int(input("Invalid input. Please enter 1, 2, or 3: "))

    play_game(human_card)