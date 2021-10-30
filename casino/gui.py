import sys, time, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QMainWindow, QSizePolicy
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, Qt
from PyQt5.QtGui import QPixmap, QIcon
from functools import partial
from cards import Deck
from game import VideoPokerGame, BlackJackGame, PAYTABLE
from playsound import playsound

CASINO_PATH = os.getenv("CASINO_PATH", "/home/ehickox/projects/casino/")

YELLOW_BUTTON_STYLE = """
    QPushButton {
    background-color: yellow;
    color: black;
    border-style: outset;
    border-width: 5px;
    border-radius: 3px;
    border-color: #ffe73c;
    padding: 6px
    padding-left 6px;
    padding-right 6px;
    }
    QPushButton::pressed
    {
    background-color: #ffe73c;
    border-style: inset;
    }
    QPushButton::checked
    {
    background-color : red;
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
            self.layout().itemAt(i).widget().setParent(None)

    def prepareMenu(self):
        self.jacksOrBetterButton = QPushButton(" JACKS OR BETTER ")
        font = self.jacksOrBetterButton.font()
        font.setPointSize(18)
        font.setBold(True)
        self.jacksOrBetterButton.setFont(font)
        self.jacksOrBetterButton.setStyleSheet(YELLOW_BUTTON_STYLE)
        self.jacksOrBetterButton.clicked.connect(self.onJacksOrBetterButtonClick)

        self.blackJackButton = QPushButton("BLACKJACK (COMING SOON)")
        font = self.blackJackButton.font()
        font.setPointSize(18)
        font.setBold(True)
        self.blackJackButton.setFont(font)
        self.blackJackButton.setStyleSheet(YELLOW_BUTTON_STYLE)
        # self.blackJackButton.clicked.connect(self.onBlackJackButtonClick)

        self.grid.addWidget(self.jacksOrBetterButton, 3, 1, QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.blackJackButton, 3, 3, QtCore.Qt.AlignCenter)
        self.update()

    def onMenuButtonClick(self):
        if self.isDealing:
            return
        if self.game.phase == "bet" and self.game.bet > 0:
            return
        if self.game.phase == "hold":
            return
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

        self.playerLabel = QLabel("PLAYER  ")
        font = self.playerLabel.font()
        font.setBold(True)
        font.setPointSize(16)
        self.playerLabel.setFont(font)
        self.grid.addWidget(self.playerLabel, 0, 1, QtCore.Qt.AlignCenter)


        self.dealerLabel = QLabel("DEALER  ")
        font = self.dealerLabel.font()
        font.setBold(True)
        font.setPointSize(16)
        self.dealerLabel.setFont(font)
        self.grid.addWidget(self.dealerLabel, 0, 3, QtCore.Qt.AlignCenter)

        # player hand
        self.cardLabels = []
        self.game.player_hand = self.game.deck.get_hand(5)
        score = str(self.game.player_hand.get_blackjack_score())
        self.playerLabel.setText("PLAYER  "+score)
        num_cards = len(self.game.player_hand.cards)
        for idx, c in enumerate(self.game.player_hand.cards):
            print(c)
            pixmap = QPixmap(c.img_path)
            im = pixmap.scaled(240, 240, QtCore.Qt.KeepAspectRatio)
            if idx == 0:
                label = QLabel()
                label.setPixmap(im)
                label.setContentsMargins(0, 0, 30*(num_cards-1), 50*(num_cards-1))
                self.cardLabels.append(label)
                label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
                label.update()
            if idx > 0 and idx < 3:
                shifty = 25
                shiftx = 30
                la = QLabel(self.cardLabels[idx-1])
                la.setPixmap(im)
                la.setContentsMargins(0, 0, 30, 25)
                p = QtCore.QPoint(shiftx, shifty)
                la.move(p)
                self.cardLabels.append(la)
                la.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                print(p)
                print(c)
                la.update()
            elif idx == 3:
                # figure out different shift pattern for second row
                shifty = 100
                shiftx = 20
                la = QLabel(self.cardLabels[0])
                la.setPixmap(im)
                la.setContentsMargins(0, 0, 30*(num_cards-1), 50*(num_cards-1))
                p = QtCore.QPoint(shiftx, shifty)
                la.move(p)
                self.cardLabels.append(la)
                la.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                print(p)
                print(c)
                la.update()
            elif idx > 3:
                shifty = 25
                shiftx = 30
                la = QLabel(self.cardLabels[idx-1])
                la.setPixmap(im)
                la.setContentsMargins(0, 0, 30, 25)
                p = QtCore.QPoint(shiftx, shifty)
                la.move(p)
                self.cardLabels.append(la)
                la.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                print(p)
                print(c)
                la.update()


        self.grid.addWidget(self.cardLabels[0], 1, 1, QtCore.Qt.AlignCenter)


        for l in self.cardLabels:
            l.update()
        # dealer hand

        self.betUpButton = QPushButton("BET 1")
        self.betUpButton.setStyleSheet("background: #ffe73c;"
                                    "color: black;")
        font = self.betUpButton.font()
        font.setPointSize(16)
        font.setBold(True)
        self.betUpButton.setFont(font)
        self.betUpButton.clicked.connect(partial(self.onBetUpButtonClick))

        self.menuButton = QPushButton("MORE GAMES")
        self.menuButton.setStyleSheet("background: #ffe73c;"
                                    "color: black;")
        font = self.menuButton.font()
        font.setPointSize(16)
        font.setBold(True)
        self.menuButton.setFont(font)
        self.menuButton.clicked.connect(partial(self.onMenuButtonClick))

        self.dealButton = QPushButton("DEAL")
        self.dealButton.setStyleSheet("background: #ffe73c;"
                                    "color: black;")
        font = self.dealButton.font()
        font.setPointSize(16)
        font.setBold(True)
        self.dealButton.setFont(font)
        self.dealButton.clicked.connect(partial(self.onDealButtonClick))

        self.creditsLabel = QLabel("CREDITS: "+str(self.game.credits))
        font = self.creditsLabel.font()
        font.setPointSize(16)
        self.creditsLabel.setFont(font)
        self.betLabel = QLabel("BET: "+str(self.game.bet))
        font = self.betLabel.font()
        font.setPointSize(16)
        self.betLabel.setFont(font)

        # spacer label
        self.grid.addWidget(QLabel(""), 4, 0)

        self.grid.addWidget(self.betUpButton, 5, 0)
        self.grid.addWidget(self.creditsLabel, 5, 1)
        self.grid.addWidget(self.menuButton, 5, 2)
        self.grid.addWidget(self.betLabel, 5, 3)
        self.grid.addWidget(self.dealButton, 5, 4)

        self.update()


    def prepareJacksOrBetter(self):
        self.game = VideoPokerGame(credits=self.global_credits)
        self.cardLabels = []
        self.holdButtons = []

        for i in range(0, 5):
            pixmap = QPixmap(CASINO_PATH + 'casino/assets/images/red_back.png')
            # im = pixmap.scaledToWidth(240)
            # im = pixmap.scaledToHeight(240)
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
            holdButtonPolicy = holdButton.sizePolicy()
            #holdButtonPolicy.setHorizontalPolicy(QSizePolicy.MinimumExpanding)
            holdButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
            holdButton.setCheckable(False)
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

        self.creditsLabel = QLabel("CREDITS: "+str(self.game.credits))
        font = self.creditsLabel.font()
        font.setPointSize(16)
        font.setBold(True)
        self.creditsLabel.setFont(font)
        self.betLabel = QLabel("BET: "+str(self.game.bet))
        font = self.betLabel.font()
        font.setPointSize(16)
        font.setBold(True)
        self.betLabel.setFont(font)

        # spacer label
        self.grid.addWidget(QLabel(""), 4, 0)

        self.grid.addWidget(self.betUpButton, 5, 0)
        self.grid.addWidget(self.creditsLabel, 5, 1)
        self.grid.addWidget(self.menuButton, 5, 2)
        self.grid.addWidget(self.betLabel, 5, 3)
        self.grid.addWidget(self.dealButton, 5, 4)

        # spacer label
        self.grid.addWidget(QLabel(""), 6, 0)

        self.update()

    def onHoldButtonClick(self, checked, idx):
        print(checked) #<- only used if the button is checkable
        print('clicked')
        print("holdButton"+str(idx)+"Click")
        if self.game.phase != "hold":
            return
        playsound(CASINO_PATH + "casino/assets/audio/click.mp3")
        if checked:
            self.game.add_hold(idx)
        else:
            self.game.remove_hold(idx)

    def onDealButtonClick(self, checked):
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
                #self.im = pixmap.scaledToWidth(120)
                # im = pixmap.scaledToHeight(240)
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
            # show only new cards plus held cards
            # show score and update credits
            self.game.draw(self.game.hold_idxs)
            score = self.game.hand.get_highest_score()
            self.isDealing = True
            for idx, l in enumerate(self.cardLabels):
                if idx not in self.game.hold_idxs:
                    pixmap = QPixmap(self.game.hand.cards[idx].img_path)
                    #self.im = pixmap.scaledToWidth(120)
                    # im = pixmap.scaledToHeight(240)
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
                print(score+"! you win "+str(winnings)+" credits!")
                self.game.credits += winnings
            else:
                self.scoreLabel.setText("PLACE A BET")
            self.isDealing = False
            self.game.change_phase("bet")

        # refresh credits and bet label
        self.creditsLabel.setText("CREDITS: "+str(self.game.credits))
        self.betLabel.setText("BET: "+str(self.game.bet))
        self.creditsLabel.update()
        self.betLabel.update()

    def onBetUpButtonClick(self, checked):
        print("betUpButtonClick")
        if self.game.phase != "bet":
            return

        if self.game.bet == 0 and self.game.credits > 0:
            self.scoreLabel.setText("PLACE A BET")
            self.scoreLabel.update()
            # new game so make the cards face back
            for idx, l in enumerate(self.cardLabels):
                pixmap = QPixmap(CASINO_PATH + 'casino/assets/images/red_back.png')
                #self.im = pixmap.scaledToWidth(120)
                # im = pixmap.scaledToHeight(240)
                im = pixmap.scaled(240, 240, QtCore.Qt.KeepAspectRatio)
                l.setPixmap(im)
                l.update()
        self.game.add_bet(1)
        print(self.game.bet)
        print(self.game.credits)
        # refresh credits and bet label
        self.creditsLabel.setText("CREDITS: "+str(self.game.credits))
        self.betLabel.setText("BET: "+str(self.game.bet))
        self.creditsLabel.update()
        self.betLabel.update()



if __name__ == '__main__':
    credits = 10
    if len(sys.argv) == 2:
        credits = int(sys.argv[1])
    app = QApplication(sys.argv)
    ex = GraphicalGame(credits)
    sys.exit(app.exec_())
