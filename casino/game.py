import os
from cards import Deck, Hand, Card
from collections import OrderedDict
from playsound import playsound
from typing import List

# Ensure CASINO_PATH is defined at the module level.
# It defaults to the directory of this file (assumed to be inside the "casino" folder).
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CASINO_PATH = os.getenv("CASINO_PATH", BASE_DIR)

PAYTABLE = OrderedDict()
PAYTABLE["royal_flush"] = 250
PAYTABLE["straight_flush"] = 50
PAYTABLE["four_of_a_kind"] = 25
PAYTABLE["full_house"] = 8
PAYTABLE["flush"] = 5
PAYTABLE["straight"] = 4
PAYTABLE["three_of_a_kind"] = 3
PAYTABLE["two_pair"] = 1 # 'Full Play Paytable is 2 here. Most Vegas casinos will do 1 here.'
PAYTABLE["pair"] = 1

class Game(object):
    def __init__(self, deck=Deck(), credits=10):
        self.deck = deck
        self.credits = credits
        self.bet = 0
        self.phase = "bet"
        self.hand = None

    def add_bet(self, amt: int):
        if amt > self.credits:
            print("error: must bet below "+str(self.credits))
            return
        if amt < 0:
            print("error: invalid bet")
            return
        self.credits -= amt
        self.bet += amt

class BlackJackGame(Game):

    def __init__(self, deck=Deck(), credits=10):
        super(BlackJackGame, self).__init__(deck=deck, credits=credits)
        self.dealer_hand = None

    def change_phase(self, p: str):
        self.phase = p
        if p == "action":
            # In action phase, the player can hit or stand.
            pass
        elif p == "bet":
            self.bet = 0

    def get_new_hand(self):
        # In blackjack the player and dealer each start with 2 cards.
        if self.phase != "bet":
            return
        # Reset deck (optional)
        self.deck.reset()
        self.hand = self.deck.get_hand(2)
        self.dealer_hand = self.deck.get_hand(2)
        self.change_phase("action")
        return self.hand, self.dealer_hand

    def hit(self):
        # Add a new card to player's hand.
        new_card = self.deck.get_hand(1).cards[0]
        self.hand.cards.append(new_card)
        return new_card

    def dealer_play(self):
        # Dealer draws until score is at least 17.
        while self.dealer_hand.get_blackjack_score() < 17:
            card = self.deck.get_hand(1).cards[0]
            self.dealer_hand.cards.append(card)
        return self.dealer_hand

    def outcome(self):
        # Returns one of: "player_bust", "dealer_bust", "player_win", "push", "player_lose"
        player_score = self.hand.get_blackjack_score()
        dealer_score = self.dealer_hand.get_blackjack_score()
        if player_score > 21:
            return "player_bust"
        if dealer_score > 21:
            return "dealer_bust"
        if player_score > dealer_score:
            return "player_win"
        elif player_score == dealer_score:
            return "push"
        else:
            return "player_lose"

class VideoPokerGame(Game):

    def __init__(self, deck=Deck(), credits=10):
        super(VideoPokerGame, self).__init__(deck=deck, credits=credits)
        self.hold_idxs = []

    def change_phase(self, p: str):
        self.phase = p
        if p == "hold":
            self.hold_idxs = []
        elif p == "bet":
            self.bet = 0

    def add_hold(self, idx: int):
        if self.phase != "hold":
            return
        if idx not in self.hold_idxs:
            self.hold_idxs.append(idx)

    def remove_hold(self, idx: int):
        if self.phase != "hold":
            return
        if idx in self.hold_idxs:
            self.hold_idxs.remove(idx)

    def get_new_hand(self):
        if self.phase != "bet":
            return
        self.hand = self.deck.get_hand()
        self.change_phase("hold")
        return self.hand

    def get_paytable_text(self) -> str:
        ret = ""
        for h, s in PAYTABLE.items():
            ret += h.replace("_", " ").upper()+" ...... "+str(s)
            ret += "\n"
        return ret

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
        self.change_phase("bet")
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
        self.add_bet(bet)
        self.get_new_hand()
        self.hand.pretty_print()
        score = self.hand.get_highest_score()
        if score:
            print(score)
            playsound(CASINO_PATH + "casino/assets/audio/pay.mp3")
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
        self.holds = []
        self.draw(holds, sound=True)
        print(self.hand)
        score = self.hand.get_highest_score()
        self.credits -= bet
        if not score:
            print("better luck next time!")
        else:
            if PAYTABLE[score] < 3:
                playsound(CASINO_PATH + "casino/assets/audio/pay2.mp3")
            elif PAYTABLE[score] >= 3 and PAYTABLE[score] < 10:
                playsound(CASINO_PATH + "casino/assets/audio/pay3.mp3")
            else:
                playsound(CASINO_PATH + "casino/assets/audio/pay4.mp3")
            winnings = PAYTABLE[score] * bet
            print(score+"! you win "+str(winnings)+" credits!")
            self.credits += winnings

    def draw(self, holds: List[int], sound=False):
        holds = set(holds)
        new_cards = self.hand.cards
        for idx, c in enumerate(self.hand.cards):
            if idx in holds:
                new_cards[idx] = c
            else:
                new_cards[idx] = self.deck.get_hand(1).cards[0]
                if sound:
                    click_path = os.path.join(CASINO_PATH, "casino/assets/audio/click.mp3")
                    playsound(click_path)
        self.hand.cards = new_cards
