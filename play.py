import time
from kuhn_poker import KuhnPoker
from kuhn_train import train
from test import Test


# Train a game tree from scratch
train(iterations=10 ** 8, saveName="kt-10M")
# Continue training from a saved file
# continueTrain('kt-10M', 90*10**6, 'kt-100M')
kt = Test()
kt.read(filepath="kt-10M")
print(kt.gameValue())

# Play against trained game tree
game = KuhnPoker()
game.read("kt-10M")
game.playAI(first=False, bank=0)
# game.read(filepath="kt-200Mp")
# game.playAI(goFirst=False, bankroll=0)
