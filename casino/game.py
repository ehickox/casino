from cards import Deck, Hand, Card
from collections import OrderedDict
from playsound import playsound

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

    def print_paytable(self):
        for h, s in PAYTABLE.items():
            print(h+"..."+str(s))

    def play(self):
        print("9/6 JACKS OR BETTER VIDEO POKER")
        self.print_paytable()
        print("\n")
        while True:
            self.play_hand()

    def play_hand(self):
        print("credits: " +str(self.credits))
        bet = input("bet> ")
        try:
            bet = int(bet)
        except Exception as e:
            exit(1)
        if bet > self.credits:
            print("error: must bet below "+str(self.credits))
            exit(0)
        self.deck.reset()
        hand = self.deck.get_hand()
        for i in hand.cards:
            playsound("click.mp3")
        print(hand)
        score = hand.get_highest_score()
        if score:
            print(score)
            playsound("pay.mp3")
        holds = []
        raw = input("cards to hold> ")
        for i in raw:
            holds.append(int(i) - 1)
        draw(self.deck, hand, holds)
        for i in holds:
            playsound("click.mp3")

        print(hand)
        score = hand.get_highest_score()
        if not score:
            print("better luck next time!")
            self.credits -= bet
        else:
            playsound("pay2.mp3")
            winnings = PAYTABLE[score] * bet
            print(score+"! you win "+str(winnings)+" credits!")
            self.credits += winnings
            self.credits -= bet


def draw(deck, hand, holds):
    new_cards = hand.cards
    for idx, c in enumerate(hand.cards):
        if idx in holds:
            new_cards[idx] = c
        else:
            new_cards[idx] = None
    for idx, c in enumerate(new_cards):
        if c is None:
            new_cards[idx] = deck.get_hand(1).cards[0]
    hand.cards = new_cards
