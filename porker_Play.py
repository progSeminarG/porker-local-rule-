from porker_Player import Player
from porker_Kawada import KawadaAI
from porker_Dealer import Card, Dealer

class Game(object):
    def __init__(self, players_list):
        self.players_list = players_list
        self.dealer = Dealer(self, players_list)

    def play(self):
        gamecont = 'continue'
        while gamecont == 'continue':
            gamecont = self.dealer.get_resp()
        print()
        print("open hands")
        self.dealer.printhands()


player1 = KawadaAI()
player2 = Player()
player3 = Player()
player4 = Player()
player5 = Player()
player6 = Player()
players_list = [player1, player2, player3, player4, player5, player6]
game = Game(players_list)
game.play()
