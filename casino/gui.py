import sys, time, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QMainWindow, QSizePolicy
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, Qt
from PyQt5.QtGui import QPixmap, QIcon
from functools import partial
from cards import Deck
from game import VideoPokerGame, BlackJackGame, PAYTABLE
from playsound import playsound

CASINO_PATH = os.getenv("CASINO_PATH", "/path/to/casino/")

YELLOW_BUTTON_STYLE = """
    QPushButton {
    background-color: yellow;
    color: black;
    border-style: outset;
    border-width: 5px;
    border-radius: 3px;
    border-color: #ffe73c;
    padding: 6px;
    padding-left: 6px;
    padding-right: 6px;
    }
    QPushButton::pressed
    {
    background-color: #ffe73c;
    border-style: inset;
    }
    QPushButton::checked
    {
    background-color: red;
    border-color: red;
    }
"""

class GraphicalGame(QWidget):

    def __init__(self, credits=10):
        super().__init__()
        self.isDealing = False
        self.global_credits = credits

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.prepareMenu()

        self.setWindowTitle("GAME PRINCE")
        self.setStyleSheet("color: #ffe73c;"
                        "background-color: #0000a0;"
                        "selection-color: #ffe73c;"
                        "selection-background-color: #0000a0;")
        self.setGeometry(0,0,1024,600)


        #self.setCursor(QtCore.Qt.BlankCursor)
        #self.showFullScreen()


        self.show()

    def clearLayout(self):
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)

    def prepareMenu(self):
        self.jacksOrBetterButton = QPushButton(" JACKS OR BETTER ")
        font = self.jacksOrBetterButton.font()
        font.setPointSize(18)
        font.setBold(True)
        self.jacksOrBetterButton.setFont(font)
        self.jacksOrBetterButton.setStyleSheet(YELLOW_BUTTON_STYLE)
        self.jacksOrBetterButton.clicked.connect(self.onJacksOrBetterButtonClick)

        self.blackJackButton = QPushButton("BLACKJACK")
        font = self.blackJackButton.font()
        font.setPointSize(18)
        font.setBold(True)
        self.blackJackButton.setFont(font)
        self.blackJackButton.setStyleSheet(YELLOW_BUTTON_STYLE)
        self.blackJackButton.clicked.connect(self.onBlackJackButtonClick)

        self.grid.addWidget(self.jacksOrBetterButton, 3, 1, QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.blackJackButton, 3, 3, QtCore.Qt.AlignCenter)
        self.update()

    def onMenuButtonClick(self):
        if self.isDealing:
            return
        if hasattr(self, "game") and self.game.phase == "bet" and self.game.bet > 0:
            return
        if hasattr(self, "game") and self.game.phase == "hold":
            return
        if hasattr(self, "game"):
            self.global_credits = self.game.credits
        self.clearLayout()
        self.prepareMenu()

    def onJacksOrBetterButtonClick(self):
        self.clearLayout()
        self.prepareJacksOrBetter()

    def onBlackJackButtonClick(self):
        self.clearLayout()
        self.prepareBlackJack()

    def prepareBlackJack(self):
        self.game = BlackJackGame(credits=self.global_credits)

        self.dealerLabel = QLabel("DEALER")
        font = self.dealerLabel.font()
        font.setBold(True)
        font.setPointSize(16)
        self.dealerLabel.setFont(font)
        self.grid.addWidget(self.dealerLabel, 0, 1, QtCore.Qt.AlignCenter)

        self.playerLabel = QLabel("PLAYER")
        font = self.playerLabel.font()
        font.setBold(True)
        font.setPointSize(16)
        self.playerLabel.setFont(font)
        self.grid.addWidget(self.playerLabel, 4, 1, QtCore.Qt.AlignCenter)

        self.scoreLabel = QLabel("")
        font = self.scoreLabel.font()
        font.setBold(True)
        font.setPointSize(16)
        self.scoreLabel.setFont(font)
        self.grid.addWidget(self.scoreLabel, 6, 1, QtCore.Qt.AlignCenter)

        self.creditsLabel = QLabel("CREDITS: " + str(self.game.credits))
        font = self.creditsLabel.font()
        font.setPointSize(16)
        self.creditsLabel.setFont(font)
        self.grid.addWidget(self.creditsLabel, 7, 0, QtCore.Qt.AlignCenter)

        self.betLabel = QLabel("BET: " + str(self.game.bet))
        font = self.betLabel.font()
        font.setPointSize(16)
        self.betLabel.setFont(font)
        self.grid.addWidget(self.betLabel, 7, 2, QtCore.Qt.AlignCenter)

        self.dealerCardLabels = []
        self.playerCardLabels = []
        for i in range(2):
            label = QLabel()
            pixmap = QPixmap(CASINO_PATH + 'casino/assets/images/red_back.png')
            im = pixmap.scaled(120, 180, QtCore.Qt.KeepAspectRatio)
            label.setPixmap(im)
            label.setScaledContents(True)
            self.dealerCardLabels.append(label)
            self.grid.addWidget(label, 1, i, QtCore.Qt.AlignCenter)
        for i in range(5):
            label = QLabel()
            pixmap = QPixmap(CASINO_PATH + 'casino/assets/images/red_back.png')
            im = pixmap.scaled(120, 180, QtCore.Qt.KeepAspectRatio)
            label.setPixmap(im)
            label.setScaledContents(True)
            self.playerCardLabels.append(label)
            self.grid.addWidget(label, 5, i, QtCore.Qt.AlignCenter)

        self.betUpButton = QPushButton("BET 1")
        self.betUpButton.setStyleSheet(YELLOW_BUTTON_STYLE)
        font = self.betUpButton.font()
        font.setPointSize(16)
        font.setBold(True)
        self.betUpButton.setFont(font)
        self.betUpButton.clicked.connect(self.onBetUpButtonClick)
        self.betUpButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.grid.addWidget(self.betUpButton, 8, 0)

        self.dealButton = QPushButton("DEAL")
        self.dealButton.setStyleSheet(YELLOW_BUTTON_STYLE)
        font = self.dealButton.font()
        font.setPointSize(16)
        font.setBold(True)
        self.dealButton.setFont(font)
        self.dealButton.clicked.connect(self.onDealButtonClick)
        self.dealButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.grid.addWidget(self.dealButton, 8, 1)

        self.hitButton = QPushButton("HIT")
        self.hitButton.setStyleSheet(YELLOW_BUTTON_STYLE)
        font = self.hitButton.font()
        font.setPointSize(16)
        font.setBold(True)
        self.hitButton.setFont(font)
        self.hitButton.clicked.connect(self.onHitButtonClick)
        self.hitButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.hitButton.setEnabled(False)
        self.grid.addWidget(self.hitButton, 9, 0)

        self.standButton = QPushButton("STAND")
        self.standButton.setStyleSheet(YELLOW_BUTTON_STYLE)
        font = self.standButton.font()
        font.setPointSize(16)
        font.setBold(True)
        self.standButton.setFont(font)
        self.standButton.clicked.connect(self.onStandButtonClick)
        self.standButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.standButton.setEnabled(False)
        self.grid.addWidget(self.standButton, 9, 1)

        self.menuButton = QPushButton("MORE GAMES")
        self.menuButton.setStyleSheet(YELLOW_BUTTON_STYLE)
        font = self.menuButton.font()
        font.setPointSize(16)
        font.setBold(True)
        self.menuButton.setFont(font)
        self.menuButton.clicked.connect(self.onMenuButtonClick)
        self.menuButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.grid.addWidget(self.menuButton, 8, 2)

        self.update()

    def updateBlackJackHands(self, hide_dealer_second=True):
        for idx, label in enumerate(self.dealerCardLabels):
            if idx < len(self.game.dealer_hand.cards):
                if idx == 1 and hide_dealer_second:
                    pixmap = QPixmap(CASINO_PATH + 'casino/assets/images/red_back.png')
                else:
                    pixmap = QPixmap(self.game.dealer_hand.cards[idx].img_path)
                im = pixmap.scaled(120, 180, QtCore.Qt.KeepAspectRatio)
                label.setPixmap(im)
                label.update()
        for idx, label in enumerate(self.playerCardLabels):
            if idx < len(self.game.hand.cards):
                pixmap = QPixmap(self.game.hand.cards[idx].img_path)
                im = pixmap.scaled(120, 180, QtCore.Qt.KeepAspectRatio)
                label.setPixmap(im)
                label.update()

    def onDealButtonClick(self, checked=False):
        if self.isDealing:
            return
        self.isDealing = True

        # Branch for Blackjack remains unchanged.
        if isinstance(self.game, BlackJackGame):
            if self.game.phase == "bet" and self.game.bet > 0:
                self.game.get_new_hand()
                self.updateBlackJackHands(hide_dealer_second=True)
                player_score = self.game.hand.get_blackjack_score()
                self.playerLabel.setText("PLAYER: " + str(player_score))
                self.hitButton.setEnabled(True)
                self.standButton.setEnabled(True)
        # Branch for Video Poker (Jacks or Better)
        else:
            # Phase "bet": deal a new hand.
            if self.game.phase == "bet" and self.game.bet > 0:
                self.game.deck.reset()
                self.game.get_new_hand()
                # Update card labels face-up with a clicking sound.
                for idx, label in enumerate(self.cardLabels):
                    pixmap = QPixmap(self.game.hand.cards[idx].img_path)
                    im = pixmap.scaled(240, 240, QtCore.Qt.KeepAspectRatio)
                    label.setPixmap(im)
                    playsound(CASINO_PATH + "casino/assets/audio/click.mp3")
                    time.sleep(0.2)
                    label.update()
                # Check for a winning hand.
                highest = self.game.hand.get_highest_score()
                if highest is not None:
                    self.scoreLabel.setText(highest.replace("_", " ").upper())
                    self.scoreLabel.update()
                    playsound(CASINO_PATH + "casino/assets/audio/pay.mp3")
                else:
                    self.scoreLabel.setText("No win")
                # Transition to drawing phase.
                self.game.change_phase("hold")

            # Phase "hold": draw new cards for unheld positions.
            elif self.game.phase == "hold":
                # Collect held card indices based on which hold buttons are toggled.
                holds = []
                for idx, btn in enumerate(self.holdButtons):
                    if btn.isChecked():
                        holds.append(idx)
                self.game.draw(holds, sound=True)
                for idx, label in enumerate(self.cardLabels):
                    pixmap = QPixmap(self.game.hand.cards[idx].img_path)
                    im = pixmap.scaled(240, 240, QtCore.Qt.KeepAspectRatio)
                    label.setPixmap(im)
                    label.update()
                # Evaluate winning hand after drawing.
                highest = self.game.hand.get_highest_score()
                if highest is not None:
                    self.scoreLabel.setText(highest.replace("_", " ").upper())
                    self.scoreLabel.update()
                    # Play payout ding based on winning level.
                    if PAYTABLE[highest] < 3:
                        playsound(CASINO_PATH + "casino/assets/audio/pay2.mp3")
                    elif PAYTABLE[highest] >= 3 and PAYTABLE[highest] < 10:
                        playsound(CASINO_PATH + "casino/assets/audio/pay3.mp3")
                    else:
                        playsound(CASINO_PATH + "casino/assets/audio/pay4.mp3")
                    winnings = PAYTABLE[highest] * self.game.bet
                    self.game.credits += winnings
                else:
                    self.scoreLabel.setText("Better luck next time!")
                self.game.change_phase("bet")
                # Reset all hold buttons (uncheck and update text).
                for btn in self.holdButtons:
                    btn.setChecked(False)
                    btn.setText("HOLD")
            # Update the credits and bet display.
            self.creditsLabel.setText("CREDITS: " + str(self.game.credits))
            self.betLabel.setText("BET: " + str(self.game.bet))

        self.isDealing = False

    def onHitButtonClick(self):
        if self.isDealing:
            return
        if isinstance(self.game, BlackJackGame) and self.game.phase == "action":
            self.isDealing = True
            self.game.hit()
            self.updateBlackJackHands(hide_dealer_second=True)
            player_score = self.game.hand.get_blackjack_score()
            self.playerLabel.setText("PLAYER: " + str(player_score))
            self.isDealing = False
            if player_score > 21:
                self.hitButton.setEnabled(False)
                self.standButton.setEnabled(False)
                self.updateBlackJackHands(hide_dealer_second=False)
                self.scoreLabel.setText("Busted! You lose.")
                self.game.change_phase("bet")
                self.global_credits = self.game.credits
    def onStandButtonClick(self):
        if self.isDealing:
            return
        if isinstance(self.game, BlackJackGame) and self.game.phase == "action":
            self.isDealing = True
            self.game.dealer_play()
            self.updateBlackJackHands(hide_dealer_second=False)
            player_score = self.game.hand.get_blackjack_score()
            dealer_score = self.game.dealer_hand.get_blackjack_score()
            result = ""
            if player_score > 21:
                result = "Busted! You lose."
            elif dealer_score > 21 or player_score > dealer_score:
                result = "You win!"
                self.game.credits += self.game.bet * 2
            elif player_score == dealer_score:
                result = "Push."
                self.game.credits += self.game.bet
            else:
                result = "Dealer wins. You lose."
            self.scoreLabel.setText(result)
            self.hitButton.setEnabled(False)
            self.standButton.setEnabled(False)
            self.game.change_phase("bet")
            self.creditsLabel.setText("CREDITS: " + str(self.game.credits))
            self.betLabel.setText("BET: " + str(self.game.bet))
            self.global_credits = self.game.credits
            self.isDealing = False

    def onBetUpButtonClick(self, checked=False):
        if isinstance(self.game, BlackJackGame):
            if self.game.phase != "bet":
                return
            if self.game.bet == 0 and self.game.credits > 0:
                self.scoreLabel.setText("PLACE A BET")
                self.scoreLabel.update()
                for label in self.dealerCardLabels:
                    pixmap = QPixmap(CASINO_PATH + 'casino/assets/images/red_back.png')
                    im = pixmap.scaled(120, 180, QtCore.Qt.KeepAspectRatio)
                    label.setPixmap(im)
                    label.update()
                for label in self.playerCardLabels:
                    pixmap = QPixmap(CASINO_PATH + 'casino/assets/images/red_back.png')
                    im = pixmap.scaled(120, 180, QtCore.Qt.KeepAspectRatio)
                    label.setPixmap(im)
                    label.update()
            self.game.add_bet(1)
            self.betLabel.setText("BET: " + str(self.game.bet))
            self.creditsLabel.setText("CREDITS: " + str(self.game.credits))
        else:
            print("betUpButtonClick")
            if self.game.phase != "bet":
                return
            if self.game.bet == 0 and self.game.credits > 0:
                self.scoreLabel.setText("PLACE A BET")
                self.scoreLabel.update()
                for idx, l in enumerate(self.cardLabels):
                    pixmap = QPixmap(CASINO_PATH + 'casino/assets/images/red_back.png')
                    im = pixmap.scaled(240, 240, QtCore.Qt.KeepAspectRatio)
                    l.setPixmap(im)
                    l.update()
            self.game.add_bet(1)
            self.creditsLabel.setText("CREDITS: " + str(self.game.credits))
            self.betLabel.setText("BET: " + str(self.game.bet))
            self.creditsLabel.update()
            self.betLabel.update()

    def prepareJacksOrBetter(self):
        self.game = VideoPokerGame(credits=self.global_credits)
        self.cardLabels = []
        self.holdButtons = []

        for i in range(0, 5):
            pixmap = QPixmap(CASINO_PATH + 'casino/assets/images/red_back.png')
            im = pixmap.scaled(240, 240, QtCore.Qt.KeepAspectRatio)
            label = QLabel()
            label.setPixmap(im)
            label.setScaledContents(True)
            self.cardLabels.append(label)
            self.grid.addWidget(label, 1, i, QtCore.Qt.AlignCenter)

        paytable_text = "JACKS OR BETTER VIDEO POKER\n"
        paytable_text += self.game.get_paytable_text()

        self.payTableLable = QLabel(paytable_text)
        font = self.payTableLable.font()
        font.setPointSize(14)
        font.setBold(True)
        self.payTableLable.setFont(font)
        self.grid.addWidget(self.payTableLable, 0, 0, 1, 2)

        self.scoreLabel = QLabel("PLACE A BET")
        font = self.scoreLabel.font()
        font.setBold(True)
        font.setPointSize(16)
        self.scoreLabel.setFont(font)
        self.grid.addWidget(self.scoreLabel, 0, 3, 1, 2)

        for i in range(0, 5):
            holdButton = QPushButton("HOLD")
            holdButton.setStyleSheet(YELLOW_BUTTON_STYLE)
            font = holdButton.font()
            font.setPointSize(16)
            font.setBold(True)
            holdButton.setFont(font)
            holdButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
            holdButton.setCheckable(True)
            holdButton.clicked.connect(partial(self.onHoldButtonClick, idx=i))
            self.holdButtons.append(holdButton)
            self.grid.addWidget(holdButton, 3, i)
            holdButton.update()

        self.betUpButton = QPushButton("BET 1")
        self.betUpButton.setStyleSheet(YELLOW_BUTTON_STYLE)
        font = self.betUpButton.font()
        font.setPointSize(16)
        font.setBold(True)
        self.betUpButton.setFont(font)
        self.betUpButton.clicked.connect(partial(self.onBetUpButtonClick))
        self.betUpButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)

        self.menuButton = QPushButton("MORE GAMES")
        self.menuButton.setStyleSheet(YELLOW_BUTTON_STYLE)
        font = self.menuButton.font()
        font.setPointSize(16)
        font.setBold(True)
        self.menuButton.setFont(font)
        self.menuButton.clicked.connect(partial(self.onMenuButtonClick))
        self.menuButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)

        self.dealButton = QPushButton("DEAL")
        self.dealButton.setStyleSheet(YELLOW_BUTTON_STYLE)
        font = self.dealButton.font()
        font.setPointSize(16)
        font.setBold(True)
        self.dealButton.setFont(font)
        self.dealButton.clicked.connect(partial(self.onDealButtonClick))
        self.dealButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)

        self.creditsLabel = QLabel("CREDITS: " + str(self.game.credits))
        font = self.creditsLabel.font()
        font.setPointSize(16)
        font.setBold(True)
        self.creditsLabel.setFont(font)
        self.betLabel = QLabel("BET: " + str(self.game.bet))
        font = self.betLabel.font()
        font.setPointSize(16)
        font.setBold(True)
        self.betLabel.setFont(font)

        self.grid.addWidget(QLabel(""), 4, 0)
        self.grid.addWidget(self.betUpButton, 5, 0)
        self.grid.addWidget(self.creditsLabel, 5, 1)
        self.grid.addWidget(self.menuButton, 5, 2)
        self.grid.addWidget(self.betLabel, 5, 3)
        self.grid.addWidget(self.dealButton, 5, 4)

        self.grid.addWidget(QLabel(""), 6, 0)
        self.update()

    def onHoldButtonClick(self, checked, idx):
        if self.game.phase != "hold":
            return
        playsound(CASINO_PATH + "casino/assets/audio/click.mp3")
        if checked:
            self.game.add_hold(idx)
            self.holdButtons[idx].setText("HELD")
        else:
            self.game.remove_hold(idx)
            self.holdButtons[idx].setText("HOLD")

    def onDealButtonClick_video(self, checked):
        print("dealButtonClick")
        if self.isDealing:
            return
        for b in self.holdButtons:
            b.setChecked(False)
            b.setCheckable(True)
        if self.game.phase == "bet" and self.game.bet > 0:
            self.game.deck.reset()
            print(len(self.game.deck.cards))
            self.game.get_new_hand()
            score = self.game.hand.get_highest_score()
            self.isDealing = True
            for idx, l in enumerate(self.cardLabels):
                pixmap = QPixmap(self.game.hand.cards[idx].img_path)
                im = pixmap.scaled(240, 240, QtCore.Qt.KeepAspectRatio)
                l.setPixmap(im)
                playsound(CASINO_PATH + "casino/assets/audio/click.mp3")
                time.sleep(0.2)
                l.update()
            if score:
                self.scoreLabel.setText(score.replace("_", " ").upper())
                self.scoreLabel.update()
                playsound(CASINO_PATH + "casino/assets/audio/pay.mp3")
            self.isDealing = False
            self.game.change_phase("hold")
        elif self.game.phase == "hold":
            print(len(self.game.deck.cards))
            self.game.draw(self.game.hold_idxs)
            score = self.game.hand.get_highest_score()
            self.isDealing = True
            for idx, l in enumerate(self.cardLabels):
                if idx not in self.game.hold_idxs:
                    pixmap = QPixmap(self.game.hand.cards[idx].img_path)
                    im = pixmap.scaled(240, 240, QtCore.Qt.KeepAspectRatio)
                    l.setPixmap(im)
                    playsound(CASINO_PATH + "casino/assets/audio/click.mp3")
                    time.sleep(0.2)
                    l.update()
            if score:
                self.scoreLabel.setText(score.upper().replace("_", " "))
                self.scoreLabel.update()
                if PAYTABLE[score] < 3:
                    playsound(CASINO_PATH + "casino/assets/audio/pay2.mp3")
                elif PAYTABLE[score] >= 3 and PAYTABLE[score] < 10:
                    playsound(CASINO_PATH + "casino/assets/audio/pay3.mp3")
                else:
                    playsound(CASINO_PATH + "casino/assets/audio/pay4.mp3")
                winnings = PAYTABLE[score] * self.game.bet
                print(score + "! you win " + str(winnings) + " credits!")
                self.game.credits += winnings
            else:
                self.scoreLabel.setText("PLACE A BET")
            self.isDealing = False
            self.game.change_phase("bet")
        self.creditsLabel.setText("CREDITS: " + str(self.game.credits))
        self.betLabel.setText("BET: " + str(self.game.bet))
        self.creditsLabel.update()
        self.betLabel.update()

if __name__ == '__main__':
    credits = 10
    if len(sys.argv) == 2:
        credits = int(sys.argv[1])
    app = QApplication(sys.argv)
    ex = GraphicalGame(credits)
    sys.exit(app.exec_())
