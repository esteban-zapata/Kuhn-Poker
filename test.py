import pickle
import random
from nodes import kNode
from anytree import Node, RenderTree

class Test():
    nodeMap: dict

    def read(self, filepath: str):
        with open(filepath, 'rb') as f:
            self.nodeMap = pickle.load(f)

    def test_play(self, testNodeMap: dict, history: str):
        cards = [1, 2, 3]
        random.shuffle(cards)
        plays = len(history)
        currentPlayer = plays % 2
        opp = 1 - currentPlayer
        if plays > 1:
            terminalPass = history[plays - 1] == 'p'
            doubleBet = history[plays - 2: plays] == 'bb'
            isPlayerCardHigher = cards[currentPlayer] > cards[opp]
            if terminalPass:
                if history == 'pp':
                    if isPlayerCardHigher:
                        return 1
                    else:
                        return -1
                else:
                    return 1
            elif doubleBet:
                if isPlayerCardHigher:
                    return 2
                else:
                    return -2
        infoSet = str(cards[currentPlayer]) + history
        if currentPlayer == 0:
            currentStrat = self.nodeMap.get(infoSet).getAvgStrat()
        else:
            currentStrat = testNodeMap.get(infoSet).getAvgStrat()
        rand = random.random()
        if rand < currentStrat[0]:
            return -self.test_play(testNodeMap, history + 'p')
        else:
            return -self.test_play(testNodeMap, history + 'b')

    def gameValue(self):
        value = 0
        cardList = [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]

        def valRecursive(self, infoSet: str) -> float:
            if infoSet not in self.nodeMap:
                node = kNode()
                node.children = infoSet
                return node.returnPayoff(cards)
            else:
                currentPlayer = (len(infoSet) - 1) % 2
                other = 1 - currentPlayer
                otherInfo = str(cards[other]) + infoSet[1:]
                strategy = self.nodeMap[infoSet].getAvgStrat()
                value = 0
                for a in range(2):
                    if a == 0:
                        value += -valRecursive(self, otherInfo + 'p') * strategy[a]
                    else:
                        value += -valRecursive(self, otherInfo + 'b') * strategy[a]
                return value

        for cards in cardList:
            value += valRecursive(self, str(cards[0])) / 6
        return value

    def exploitability(self) -> list:
        gt = self.bestResponse()
        output = [0, 0]
        for b in range(1, 4):
            output[0] += gt[str(b)]['ev'] / 3
            output[1] -= gt[str(b)]['br'] / 3
        return output


    def bestResponse(self) -> dict:
        def traverseing(self, history: str, reachProb: dict, gameTree: dict) -> dict:
            currentPlayer = len(history) % 2
            otherPlayer = 1 - currentPlayer
            childCards = {"1": ["2", "3"], "2": ["1", "3"], "3": ["1", "2"]}
            possibleCards = ["1", "2", "3"]
            if history == 'pb':
                x = 1
            for n in ['p', 'b']:
                a = ['p', 'b'].index(n)
                if isTerminal(history + n):
                    for card in possibleCards:
                        if card + history == '1p':
                            x = 1
                        brTemp = 0
                        evTemp = 0
                        npEV = 0
                        npBR = 0
                        for other in childCards[card]:
                            evCards = [int(card), int(other)] if currentPlayer == 1 else [int(other), int(card)]
                            brCards = [int(card), int(other)] if currentPlayer == 0 else [int(other), int(card)]
                            evRP = other + str(currentPlayer)
                            brRP = other + str(otherPlayer)
                            evNextNode = kNode()
                            evNextNode.children = card + history + n
                            evCurrentNode = self.nodeMap[other + history]
                            evTemp += reachProb[evRP] * evCurrentNode.getAvgStrat()[a] * (-evNextNode.returnPayoff(evCards))
                            npEV += reachProb[evRP]
                            brNextNode = kNode()
                            brNextNode.children = other + history + n
                            brTemp += reachProb[brRP] * (-brNextNode.returnPayoff(brCards))
                            npBR += reachProb[brRP]
                        if npEV != 0:
                            evTemp /= npEV
                        gameTree[card + history]['ev'] += evTemp
                        if npBR != 0:
                            brTemp /= npBR
                        if 'br' not in gameTree[card + history]:
                            gameTree[card + history]['br'] = brTemp
                        else:
                            gameTree[card + history]['br'] = max(gameTree[card + history]['br'], brTemp)
                else:
                    # update possible moves
                    newRP = {}
                    for card in possibleCards:
                        currentNode = self.nodeMap[card + history]
                        if currentPlayer == 0:
                            newRP[card + '0'] = reachProb[card + '0'] * currentNode.getAvgStrat()[a]
                            newRP[card + '1'] = reachProb[card + '1']
                        else:
                            newRP[card + '0'] = reachProb[card + '0']
                            newRP[card + '1'] = reachProb[card + '1'] * currentNode.getAvgStrat()[a]
                    gameTree = traverseing(self, history + n, newRP, gameTree)
                    for card in possibleCards:
                        evTemp = 0
                        if 'br' not in gameTree[card + history]:
                            gameTree[card + history]['br'] = -gameTree[card + history + n]['ev']
                        else:
                            gameTree[card + history]['br'] = max(gameTree[card + history]['br'], -gameTree[card + history + n]['ev'])
                        npEV = 0
                        for other in childCards[card]:
                            currentNode = self.nodeMap[other + history]
                            evRP = other + str(currentPlayer)
                            npEV += reachProb[evRP]
                            evTemp += reachProb[evRP] * currentNode.getAvgStrat()[a] * -gameTree[card + history + n]['br']
                        if npEV != 0: evTemp /= npEV
                        gameTree[card + history]['ev'] += evTemp
            return gameTree
        rp = {}
        RPList = ['10', '11', '20', '21', '30', '31']
        for card in RPList:
            rp[str(card)] = 1
        return traverseing(self, '', rp, treeBuilder())

    def prune(self, threshold: str):
        for item in self.nodeMap:
            self.nodeMap[item].promisingBranch = list(range(2))
            for i in range(2):
                if self.nodeMap[item].regretSum[i] < threshold:
                    self.nodeMap[item].promisingBranch.remove(i)


def isTerminal(history: str) -> bool:
    return history == 'pp' or history == 'pbp' or history == 'pbb' or history == 'bp' or history == 'bb'


def treeBuilder():
    nodeMap = {}
    for card in range(1, 4):
        infoSet = str(card)
        for strategy in ['', 'p', 'b', 'pb']:
            IS = infoSet + strategy
            nodeMap[IS] = {'ev': 0}
    return nodeMap

def printTree(tree: dict):
    root = Node("root")
    nodes = {"root": root}
    for item in tree:
        parent = nodes["root"]
        for i in range(len(item)):
            key = item[:i+1]
            if key not in nodes:
                nodes[key] = Node(key, parent=parent)
            parent = nodes[key]
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

def buildAvgStrat():
    nodeMap = {}
    for card in range(1, 4):
        history = str(card)
        infoSet = history
        currentNode = kNode()
        currentNode.children = infoSet
        nodeMap[infoSet] = currentNode
        for strategy in ['', 'p', 'b', 'pb']:
            infoSet = history + strategy
            currentNode = kNode()
            currentNode.children = infoSet
            nodeMap[infoSet] = currentNode
    return nodeMap

if __name__ == '__main__':
    game = Test()
    nodeMap = buildAvgStrat()
    game.nodeMap = nodeMap
    printTree(game.nodeMap)
    exp = game.bestResponse()
    printTree(exp)
    for i in exp:
        print(f'{i}: {exp[i]}')
    print(f'best response: {exp}')
    print(f'game value: {game.gameValue()}')
    print(game.exploitability())
    print(game.bestResponse())
