import random

class Player(object):
    def __init__(self):
        self.my_cards = []

    def get_know_dealer(self, dealer_input):
        self.dealer = dealer_input

    def get_hand(self, dealer_input):
        self.my_cards = self.my_cards + dealer_input
        # print([card.card for card in self.my_cards])

    def restore_cards(self):
        ls = [0, 1, 2, 3, 4]
        num = random.randint(1,5)
        ret = sorted(random.sample(ls, num))
        restore = []
        [restore.append(self.my_cards.pop(num-1-i)) for i in range(0,num)]
        return restore

    def respond(self):
        ret = ['call']*1+['stay']*99
        ret = ret[random.randint(0,len(ret)-1)]
        return ret
