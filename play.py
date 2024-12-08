# ML Project
# Esteban Zapata & Raxel Ortiz
import time
from kuhn_poker import KuhnPoker
from kuhn_train import continueTrainPrune, train, continueTrain
from test import Test


# Train a game tree from scratch
# train(iterations=10 ** 7, saveName="kt-10M")
# Continue training from a saved file
continueTrainPrune('kt-10M',10**6, 'kt-100M')
kt = Test()
kt.read(filepath="kt-100M")
# print(kt.gameValue())

# Play against trained game tree
game = KuhnPoker()
game.read("kt-100M")
game.playAI(first=False, bank=0)
# game.read(filepath="kt-200Mp")
# game.playAI(goFirst=False, bankroll=0)
