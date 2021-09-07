from cards import Deck, Hand, Card

PAYTABLE = {
    "straight_flush": 50,
    "four_of_a_kind": 25,
    "full_house": 7,
    "flush": 5,
    "straight": 4,
    "three_of_a_kind": 3,
    "two_pair": 2,
    "pair": 1
}

class Game(object):

    def __init__(self, deck=Deck(), credits=10):
        self.deck = deck
        self.credits = credits

    def play(self):
        while True:
            self.play_hand()

    def play_hand(self):
        print("credits:" +str(self.credits))
        bet = input("bet> ")
        try:
            bet = int(bet)
        except Exception as e:
            exit(1)
        if bet > self.credits:
            print("error: must bet below "+str(self.credits))
            exit(0)
        self.deck.reset()
        h = self.deck.get_hand()
        print(h)
        holds = []
        raw = input("cards to hold> ")
        for i in raw:
            holds.append(int(i) - 1)
        draw(self.deck, h, holds)
        print(h)
        score = h.get_highest_score()
        if not score:
            print("better luck next time!")
            self.credits -= bet
        else:
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
