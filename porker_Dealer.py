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
        self.first_handout_cards()
        self.__field_cards = []

    def deack_reset(self):
        print(len(self.__handling_cards))
        if len(self.__handling_cards) < 5:
            self.__handling_cards = self.__handling_cards + self.__field_cards
            self.__field_cards = []

    def __create_all_cards_stack(self):
        self.__all_cards = []
        for inumber in range(self.__MIN_NUMBER_CARDS,
                             self.__MAX_NUMBER_CARDS+1):
            for suit in self.__SUITE:
                self.__all_cards.append(Card(suit, inumber))

    def first_handout_cards(self):
        self.__players_cards = []
        for player in self.__players:
            able_num =len(self.__handling_cards)
            self.__players_cards.append([self.__handling_cards.pop(able_num-1-i) for i in
                                         range(self.__NUM_HAND)])
            player.get_hand(self.__players_cards[-1])

    def handout_cards(self, player, num):
        car = []
        able_num = len(self.__handling_cards)
        car.append([self.__handling_cards.pop(able_num-1-i) for i in range(num)])
        print([card.card for card in car[-1]])
        player.get_hand(car[-1])

    def get_resp(self):
        for player in self.__players:
            resp = player.restore_cards()
            self.__field_cards = self.__field_cards + resp[1]
            self.handout_cards(player, resp[0])
            player.respond()
            self.deack_reset()


    def restore(self):
        for player in self.__players:
            player.restore_cards()

    def get_respond(self):
        for player in self.__players:
            player.respond()
