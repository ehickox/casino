from cards import Deck, Hand, Card
from collections import OrderedDict
from playsound import playsound
from typing import List

PAYTABLE = OrderedDict()
PAYTABLE["royal_flush"] = 500
PAYTABLE["straight_flush"] = 50
PAYTABLE["four_of_a_kind"] = 25
PAYTABLE["full_house"] = 9
PAYTABLE["flush"] = 6
PAYTABLE["straight"] = 4
PAYTABLE["three_of_a_kind"] = 3
PAYTABLE["two_pair"] = 1
PAYTABLE["pair"] = 1

class Game(object):

    def __init__(self, deck=Deck(), credits=10):
        self.deck = deck
        self.credits = credits
        self.bet = 0
        self.phase = "bet"
        self.hand = None

    def change_phase(self, p: str):
        self.phase = p

    def add_bet(self, amt: int):
        if amt > self.credits:
            print("error: must bet below "+str(self.credits))
            return
        if amt < 0:
            print("error: invalid bet")
            return
        self.credits -= amt
        self.bet += amt

    def get_new_hand(self):
        if self.phase != "bet":
            return
        self.hand = self.deck.get_hand()
        self.phase = "hold"

    def print_paytable(self):
        for h, s in PAYTABLE.items():
            print(h+"..."+str(s))

    def play_term(self):
        print("9/6 JACKS OR BETTER VIDEO POKER")
        self.print_paytable()
        print("\n")
        while True:
            self.play_hand_term()

    def play_hand_term(self):
        self.deck.reset()
        print("credits: " +str(self.credits))
        bet = input("bet> ")
        try:
            bet = int(bet)
        except Exception as e:
            return
        if bet > self.credits:
            print("error: must bet below "+str(self.credits))
            return
        if bet < 0:
            print("error: invalid bet")
            return
        hand = self.deck.get_hand()
        hand.pretty_print()
        score = hand.get_highest_score()
        if score:
            print(score)
            playsound("assets/audio/pay.mp3")
        holds = []
        while True:
            raw = input("cards to hold> ")
            try:
                for i in raw:
                    ho = int(i)
                    if ho >=1 and ho <= 5:
                        holds.append(ho - 1)
                    else:
                        raise Exception("error: out of range")
            except Exception as e:
                holds = []
                continue
            else:
                break

        draw(self.deck, hand, holds)
        print(hand)
        score = hand.get_highest_score()
        self.credits -= bet
        if not score:
            print("better luck next time!")
        else:
            if PAYTABLE[score] < 3:
                playsound("assets/audio/pay2.mp3")
            elif PAYTABLE[score] >= 3 and PAYTABLE[score] < 10:
                playsound("assets/audio/pay3.mp3")
            else:
                playsount("pay4.mp3")
            winnings = PAYTABLE[score] * bet
            print(score+"! you win "+str(winnings)+" credits!")
            self.credits += winnings


def draw(deck: Deck, hand: Hand, holds: List):
    holds = set(holds)
    new_cards = hand.cards
    for idx, c in enumerate(hand.cards):
        if idx in holds:
            new_cards[idx] = c
        else:
            new_cards[idx] = None
    for idx, c in enumerate(new_cards):
        if c is None:
            new_cards[idx] = deck.get_hand(1).cards[0]
            playsound("assets/audio/click.mp3")
    hand.cards = new_cards
