import random
import time
import sys, os
import requests
from collections import defaultdict
from playsound import playsound
from colorama import Style
from colorama import Fore

card_order_dict = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10,"J":11, "Q":12, "K":13, "A":14}

class Card(object):

    def __init__(self, suit, numerical_value, name, symbol=None):
        casino_path = os.getenv("CASINO_PATH", "/home/ehickox/projects/casino")
        self.suit = suit
        self.numerical_value = numerical_value
        self.name = name
        self.symbol = symbol
        self.value = str(numerical_value)
        if numerical_value > 10:
            self.value = name[0].upper()
        self.img_path = casino_path + "/casino/assets/images/"+str(self.value)+self.suit[0].upper()+".png"
        self.blackjack_value = numerical_value

        if name in ["jack", "queen", "king"]:
            self.blackjack_value = 10
        if name == "ace":
            self.blackjack_value = 1

    def __repr__(self):
        return self.value + " " +self.symbol

class Deck(object):

    def __init__(self, cards=[]):
        self.cards = cards
        self.reset()

    def reset(self):
        self.cards = []
        for i in range(2, 11):
            self.cards.append(Card("heart", i, str(i), f"{Fore.RED}♥{Style.RESET_ALL}"))

        self.cards.append(Card("heart", 11, "jack", f"{Fore.RED}♥{Style.RESET_ALL}"))
        self.cards.append(Card("heart", 12, "queen", f"{Fore.RED}♥{Style.RESET_ALL}"))
        self.cards.append(Card("heart", 13, "king", f"{Fore.RED}♥{Style.RESET_ALL}"))
        self.cards.append(Card("heart", 14, "ace", f"{Fore.RED}♥{Style.RESET_ALL}"))
        for i in range(2, 11):
            self.cards.append(Card("diamond", i, str(i), f"{Fore.RED}♦{Style.RESET_ALL}"))

        self.cards.append(Card("diamond", 11, "jack", f"{Fore.RED}♦{Style.RESET_ALL}"))
        self.cards.append(Card("diamond", 12, "queen", f"{Fore.RED}♦{Style.RESET_ALL}"))
        self.cards.append(Card("diamond", 13, "king", f"{Fore.RED}♦{Style.RESET_ALL}"))
        self.cards.append(Card("diamond", 14, "ace", f"{Fore.RED}♦{Style.RESET_ALL}"))
        for i in range(2, 11):
            self.cards.append(Card("club", i, str(i), f"{Fore.BLACK}♣{Style.RESET_ALL}"))

        self.cards.append(Card("club", 11, "jack", f"{Fore.BLACK}♣{Style.RESET_ALL}"))
        self.cards.append(Card("club", 12, "queen", f"{Fore.BLACK}♣{Style.RESET_ALL}"))
        self.cards.append(Card("club", 13, "king", f"{Fore.BLACK}♣{Style.RESET_ALL}"))
        self.cards.append(Card("club", 14, "ace", f"{Fore.BLACK}♣{Style.RESET_ALL}"))
        for i in range(2, 11):
            self.cards.append(Card("spade", i, str(i), f"{Fore.BLACK}♠{Style.RESET_ALL}"))

        self.cards.append(Card("spade", 11, "jack", f"{Fore.BLACK}♠{Style.RESET_ALL}"))
        self.cards.append(Card("spade", 12, "queen", f"{Fore.BLACK}♠{Style.RESET_ALL}"))
        self.cards.append(Card("spade", 13, "king", f"{Fore.BLACK}♠{Style.RESET_ALL}"))
        self.cards.append(Card("spade", 14, "ace", f"{Fore.BLACK}♠{Style.RESET_ALL}"))

        random.shuffle(self.cards)

    def get_hand(self, num_cards=5):
        hand = random.sample(self.cards, num_cards)
        self.cards = [c for c in self.cards if c not in hand]
        return Hand(hand)

    def shuffle(self):
        beacon_resp = requests.get("https://beacon.nist.gov/beacon/2.0/pulse/last")
        rand_seed = beacon_resp.json()["pulse"]["outputValue"]
        random.seed(rand_seed)
        random.shuffle(self.cards)

    def __repr__(self):
        ret = ""
        for c in self.cards:
            ret += str(c)
        return ret


class Hand(object):

    def __init__(self, cards):
        self.cards = cards

    def get_blackjack_score(self):
        total = 0
        ace_found = False
        soft = False

        for card in self.cards:
            total += card.blackjack_value

            if card.blackjack_value == 1:
                ace_found = True

        if total < 12 and ace_found:
            total += 10
            soft = True

        return total

    def check_bust(self):
        return self.get_blackjack_score() > 21

    def get_highest_score(self):
        if self.check_royal_flush():
            return "royal_flush"
        elif self.check_straight_flush():
            return "straight_flush"
        elif self.check_four_of_kind():
            return "four_of_a_kind"
        elif self.check_full_house():
            return "full_house"
        elif self.check_flush():
            return "flush"
        elif self.check_straight():
            return "straight"
        elif self.check_three_of_kind():
            return "three_of_a_kind"
        elif self.check_two_pairs():
            return "two_pair"
        elif self.check_pair():
            return "pair"
        else:
            return None

    def check_pair(self, jacks_or_better=True):
        for idx, c in enumerate(self.cards):
            if c.numerical_value >= 11 or not jacks_or_better:
                h_temp = self.cards.copy()
                del h_temp[idx]
                for cc in h_temp:
                    if c.numerical_value == cc.numerical_value:
                        return True
        return False

    def check_two_pairs(self):
        values = [i.value for i in self.cards]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v]+=1
        if sorted(value_counts.values())==[1,2,2]:
            return True
        else:
            return False

    def check_three_of_kind(self):
        values = [i.value for i in self.cards]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v]+=1
        if set(value_counts.values()) == set([3,1]):
            return True
        return False

    def check_four_of_kind(self):
        values = [i.value for i in self.cards]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v]+=1
        if set(value_counts.values()) == set([4,1]):
            return True
        return False

    def check_full_house(self):
        values = [i.value for i in self.cards]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v]+=1
        if sorted(value_counts.values()) == [2,3]:
            return True
        return False

    def check_flush(self):
        suits = [c.suit for c in self.cards]
        if len(set(suits)) == 1:
          return True
        return False

    def check_straight(self):
        values = [i.value for i in self.cards]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v] += 1
        rank_values = [card_order_dict[i] for i in values]
        value_range = max(rank_values) - min(rank_values)
        if len(set(value_counts.values())) == 1 and (value_range==4):
            return True
        else:
            #check straight with low Ace
            if set(values) == set(["A", "2", "3", "4", "5"]):
                return True
            return False

    def check_straight_flush(self):
        if self.check_flush() and self.check_straight():
            return True
        return False

    def check_royal_flush(self):
        if not self.check_straight_flush():
            return False
        return all(x in values for x in ["A", "K", "Q", "J", "10"])

    def pretty_print(self):
        for i, c in enumerate(self.cards):
            playsound("assets/audio/click.mp3")
            if i == 0:
                sys.stdout.write("| "+str(c)+" |")
            else:
                sys.stdout.write(" "+str(c)+" |")
            sys.stdout.flush()
            time.sleep(0.05)

        sys.stdout.write("\n")
        sys.stdout.flush()

        ret = "|"
        for idx, c in enumerate(self.cards):
            if c.numerical_value == 10:
                ret += "  "+str(idx + 1)+"   |"
            else:
                ret += "  "+str(idx + 1)+"  |"
        print(ret)

    def __repr__(self):
        ret = "|"
        for c in self.cards:
            ret += " "+str(c)+" |"
        ret += "\n"
        ret += "|"
        for idx, c in enumerate(self.cards):
            if c.numerical_value == 10:
                ret += "  "+str(idx + 1)+"   |"
            else:
                ret += "  "+str(idx + 1)+"  |"
        return ret
