# ! /usr/bin/env python3

import random
import sys
from copy import deepcopy
import collections


class Card(object):
    def __init__(self, suit, number):
        if suit not in ("S", "C", "H", "D"):
            # S: spade, C: club, H: heart, D: Diamond
            raise ValueError("ERROR: suit of card is not correct: "
                             + str(suit))
        self.__suit = suit
        if number not in range(1, 14):
            raise ValueError("ERROR: number of card is not correct: "
                             + str(number))
        self.__number = number

    @property
    def card(self):
        return (self.__suit, self.__number)

    @property
    def suit(self):
        return self.__suit

    @property
    def number(self):
        return self.__number


class Dealer(object):
    def __init__(self, game_inst, players_input):
        # FIXED PARAMETERS
        self.__MIN_NUMBER_CARDS = 1  # smallest number of playing cards
        self.__MAX_NUMBER_CARDS = 13  # largest number of playing cards
        self.__SUITE = ['S', 'C', 'H', 'D']  # suit of playing cards
        self.__NUM_HAND = 5
        self.__game_inst = game_inst
        self.__players = deepcopy(players_input)  # instance of players
        self.__num_players = len(self.__players)  # number of players ~8
        self.__create_all_cards_stack()
        self.__handling_cards = self.__all_cards
        self.__playershands = [None]*len(self.__players)
        random.shuffle(self.__handling_cards)
        self.first_handout_cards()
        self.__field_cards = []
        self.__callcheck = False
        self.__after_call_flag = 0

    @property
    def names_of_players(self):
        return [i.__class__.__name__ for i in self.__players]

    def deack_reset(self):  # dealerのカードが減ったら場のカードを回収して補充する
        if len(self.__handling_cards) < 5:
            self.__handling_cards = self.__handling_cards + self.__field_cards
            random.shuffle(self.__handling_cards)
            self.__field_cards = []
            print("deack_reset")

    def __create_all_cards_stack(self):
        self.__all_cards = []
        for inumber in range(self.__MIN_NUMBER_CARDS,
                             self.__MAX_NUMBER_CARDS+1):
            for suit in self.__SUITE:
                self.__all_cards.append(Card(suit, inumber))

    def first_handout_cards(self):
        i = 0
        self.__players_cards = []
        for player in self.__players:
            able_num =len(self.__handling_cards)
            self.__players_cards.append([self.__handling_cards.pop(able_num-1-i) for i in
                                         range(self.__NUM_HAND)])
            self.__playershands[i] = self.__players_cards[-1]
            player.get_hand(self.__players_cards[-1])

    def printhands(self):
        for i in range(len(self.__players)):
            print(self.names_of_players[i])
            print([card.card for card in self.__players_cards[i]])
            print(self.calc_hand_score(self.__players_cards[i]))
            print()

    def handout_cards(self, player, playernum, num):
        car = []
        able_num = len(self.__handling_cards)
        car.append([self.__handling_cards.pop(able_num-1-i) for i in range(num)])
        # print([card.card for card in car[-1]])
        self.__players_cards[playernum] = self.__players_cards[playernum]+car[-1]
        player.get_hand(car[-1])

    def get_resp(self):
        i = 0
        for player in self.__players:
            print(self.names_of_players[i])
            resp = player.restore_cards()
            self.restore(i, resp)
            self.__field_cards = self.__field_cards + resp
            self.handout_cards(player, i, len(resp))
            if self.__callcheck is False:
                if player.respond() == 'call':
                    self.__callcheck = True
            else:
                self.__after_call_flag = self.__after_call_flag + 1
                if self.__after_call_flag == len(self.__players) - 1:
                    return 'end'
            print()
            self.deack_reset()
            i = i+1
        return 'continue'

    def restore(self, playernum, resp):
        print([card.card for card in resp])
        for i in range(len(resp)):
            for j in range(len(self.__players_cards[playernum])):
                if resp[i] == self.__players_cards[playernum][j]:
                    rest = j
            self.__players_cards[playernum].pop(rest)





    # calculate best score from given set of cards
    # 担当：白井．7枚のカードリストを受け取り，役とベストカードを返します．
    def calc_hand_score(self, cards):  # 7カードリストクラスをもらう
        SS = ['S', 'C', 'H', 'D']
        suit_list = [0, 0, 0, 0]
        (num, suit, card_list) = self.choice(cards)
        # クラスからnum, suit, cardを抜き出す
        pp = self.checkpair(cards)
        # REPLACE 1-->14
        num = self.rpc1(num)
        num.sort()
        nc = self.rpcards1(card_list)
        card_list = nc
        card_list = sorted(card_list, key=lambda x: x[1])  # 2ndでsort

        flash = 0
        straight = 0
        straight_flash = 0
        # for flash:make flash_list
        for SUIT in SS:
            if suit.count(SUIT) >= 5:  # flash
                flash = 1
                flash_list = []
        straight = self.stlist(card_list)
        if straight == 1 and flash == 1:
            score = 8
            straight_flash = 1

        # == JUDGE BELOW ==
        # Straight-Flash
        # 4cards
        elif pp[0] >= 1:
            score = 7
        # Fullhouse
        elif pp[1] == 2:  # 3c *2
            score = 6
            c = 0
            for i in range(self.__MAX_NUMBER_CARDS):
                if num.count(14-i) == 3:
                    for n in range(len(card_list)):
                        if card_list[n][1] == (14-i):
                            c += 1
                            if c == 2:  # 小さい方の3cは2個だけ取る
                                break
        elif pp[1] == 1 and pp[2] >= 1:  # 3c+pair
            score = 6
        # Flash
        elif flash == 1:
            score = 5
        # Straight
        elif straight == 1:
            score = 4
        # 3cards
        elif pp[1] == 1:
            score = 3
        # 2pairs
        elif pp[2] >= 2:
            score = 2
            c = 0
            for i in range(self.__MAX_NUMBER_CARDS):
                if num.count(14-i) == 2 and c != 2:
                    c += 1
        # 1pair
        elif pp[2] == 1:
            score = 1
            # no pair
        else:
            score = 0
        return score

    # for: calc_hand_score
    def choice(self, card_list):  # suit, num, cardのみを取り出してリスト化
        SS = ['S', 'C', 'H', 'D']
        suit = [0]*len(card_list)
        num = [0]*len(card_list)
        card = [0]*len(card_list)
        for i in range(len(card_list)):
            num[i] = card_list[i].number
            suit[i] = card_list[i].suit
            card[i] = card_list[i].card
        return (num, suit, card)

    # for straight:make straight_list
    def stlist(self, card_list):
        card_list = sorted(card_list, key=lambda x: x[1])
        num = [0]*len(card_list)
        for i in range(len(card_list)):
            num[i] = card_list[i][1]
        straight_list = []
        straight = 0
        num_list = [0]*15
        for card in num:  # 数字の個数カウント
            num_list[card] += 1
        for i in range(10):
            prod = num_list[14-i]*num_list[13-i] *\
                num_list[12-i]*num_list[11-i]*num_list[10-i]
            if prod >= 1:
                straight = 1  # st宣言
                break
        return straight

    # Kawadaさんのもの
    def checkpair(self, any_cards):  # ペアの評価方法
        pair = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # A~Kまでの13個のリスト要素を用意
        for i in range(0, len(any_cards)):  # カードの枚数ぶんだけ試行
            pair[any_cards[i].number-1] = \
                pair[any_cards[i].number-1]+1
                # カードのnumber要素を参照し先ほどのリストpairの対応要素のカウントを1つ増やす
        pairs = [0, 0, 0]  # pairsは[4カード有無, 3カードの有無, ペアの数]のリスト
        for i in range(0, self.__MAX_NUMBER_CARDS):  # pairの要素A~13すべて順に参照
            if pair[i] == 4:  # lその要素が４枚あるときpairs[0]のカウントを増やす
                pairs[0] = pairs[0]+1
            elif pair[i] == 3:  # 同様に3枚
                pairs[1] = pairs[1]+1
            elif pair[i] == 2:  # 同様に2枚
                pairs[2] = pairs[2]+1
        return pairs  # pairsは[4カード有無, 3カードの有無, ペアの数]のリスト

    def rpc1(self, cards):  # 最初に1-->14にする方 引数はリスト
        rp = []
        for card in cards:
            card = (card+11) % 13 + 2
            rp.append(card)
        return rp

    def rpc2(self, cards):  # 最後に14-->1に戻す方 引数はリスト
        rp = []
        for card in cards:
            card = (card-1) % 13 + 1
            rp.append(card)
        return rp

    def rpcards1(self, cards):  # 最初に1-->14にする方 引数はカードタプルリスト
        nc = []
        for i in range(len(cards)):
            ss = cards[i][0]
            nn = (cards[i][1]+11) % 13 + 2
            nc.append((ss, nn))
        return nc

    def rpcards2(self, cards):  # 最後に14-->1に戻す方 引数はカードタプルリスト
        nc = []
        for i in range(len(cards)):
            ss = cards[i][0]
            nn = (cards[i][1]-1) % 13 + 1
            nc.append((ss, nn))
        return nc
