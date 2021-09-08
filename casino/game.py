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
            return
        if bet > self.credits:
            print("error: must bet below "+str(self.credits))
            return
        if bet < 0:
            print("error: invalid bet")
            return
        self.deck.reset()
        hand = self.deck.get_hand()
        hand.pretty_print()
        score = hand.get_highest_score()
        if score:
            print(score)
            playsound("pay.mp3")
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

        holds = set(holds)
        draw(self.deck, hand, holds)
        print(hand)
        score = hand.get_highest_score()
        if not score:
            print("better luck next time!")
            self.credits -= bet
        else:
            if PAYTABLE[score] < 3:
                playsound("pay2.mp3")
            elif PAYTABLE[score] >= 3 and PAYTABLE[score] < 10:
                playsound("pay3.mp3")
            else:
                playsount("pay4.mp3")
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
            playsound("click.mp3")
    hand.cards = new_cards
