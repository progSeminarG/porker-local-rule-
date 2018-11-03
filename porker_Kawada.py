import random
import itertools
from porker_Dealer import Card
from operator import itemgetter

class Player(object):
    def __init__(self):
        self.my_cards = []

    def get_hand(self, dealer_input):
        self.my_cards = self.my_cards + dealer_input
        print([card.card for card in self.my_cards])

    def restore_cards(self):
        print([card.card for card in self.my_cards])
        ls = [0, 1, 2, 3, 4]
        num = random.randint(1,5)
        ret = sorted(random.sample(ls, num))
        restore = []
        [restore.append(self.my_cards.pop(num-1-i)) for i in range(0,num)]
        return restore

    def respond(self):
        ret = ['call']+['stay']*99
        ret = ret[random.randint(0,len(ret)-1)]
        return ret


class KawadaAI(Player):
    def get_hand(self, dealer_input):
        self.my_cards = self.my_cards + dealer_input
        print([card.card for card in self.my_cards])

    def know_not_open_card(self):
        self.field = self.dealer.field_cards()
        self.not_open = self.subtract_list(self.dealer.all_cards, self.field)
        self.not_open = self.subtract_list(self.not_open, self.my_cards)

    def get_know_dealer(self, dealer_input):
        self.dealer = dealer_input

    def restore_cards(self):
        new_my_cards = self.think_percentage()
        restore = self.subtract_list(self.my_cards, new_my_cards)
        self.my_cards = new_my_cards
        return restore

    def respond(self):
        ret = ['call']*0+['stay']*99
        ret = ret[random.randint(0,len(ret)-1)]
        if self.calc_hand_score(self.my_cards) >= 3:
            ret = 'call'
        return ret

    def think_percentage(self):
        basescore = self.calc_hand_score(self.my_cards)
        self.know_not_open_card()
        ok_list = []
        for i in range (0, 5):
            possible_list = list(itertools.combinations(self.my_cards, i))
            possible_dlaw = list(itertools.combinations(self.not_open, 5-i))
            for j in range(len(possible_list)):
                scores = []
                for k in range(len(possible_dlaw)):
                    score  = self.calc_hand_score(possible_list[j]+possible_dlaw[k])
                    scores.append(score)
                    '''if score < basescore:
                        break'''
                    if k == len(possible_dlaw)-1:
                        ok_list.append([possible_list[j], sum(scores)*100/k])
        if len(ok_list)==0:
            return [self.my_cards[0]]
        return list(sorted(ok_list, key=itemgetter(1))[-1][0])

    def tuple_to_list(self, tuple):
        makelist = []
        for i in range(len(tuple)):
            makelist.append(tuple[i])
        return makelist

    def subtract_list(self, list1, list2):  # list1からlist2の要素を削除したリストを作成
        retlist = []
        poplist = []
        for i in range(len(list2)):
            for j in range(len(list1)):
                if list2[i].card == list1[j].card:
                    poplist.append(j)
                    break
        poplist.sort()
        poplist.append(100)
        j=0
        for i in range(len(list1)):
            if i != poplist[j]:
                retlist.append(list1[i])
            else:
                j = j+1
        return retlist

    # 以下callの目安、手持ちのスコアを計算する
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
            for i in range(13):
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
            for i in range(13):
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
        for i in range(0, 13):  # pairの要素A~13すべて順に参照
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
