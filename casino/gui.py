import sys, time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QMainWindow, QSizePolicy
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, Qt
from PyQt5.QtGui import QPixmap, QIcon
from functools import partial
from cards import Deck
from game import Game, PAYTABLE
from playsound import playsound

class GraphicalGame(QWidget):

    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.game = Game()
        self.cardLabels = []
        self.holdButtons = []

        for i in range(0, 5):
            pixmap = QPixmap('assets/images/red_back.png')
            # im = pixmap.scaledToWidth(240)
            # im = pixmap.scaledToHeight(240)
            im = pixmap.scaled(240, 240, QtCore.Qt.KeepAspectRatio)
            label = QLabel()
            label.setPixmap(im)
            label.setScaledContents(True)
            self.cardLabels.append(label)
            self.grid.addWidget(label, 1, i, QtCore.Qt.AlignCenter)

        paytable_text = "9/6 JACKS OR BETTER VIDEO POKER\n"
        paytable_text += self.game.get_paytable_text()

        self.payTableLable = QLabel(paytable_text)
        font = self.payTableLable.font()
        font.setPointSize(16)
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
            holdButton.setStyleSheet("background-color: #ffe73c;"
                                    "color: black;")
            font = holdButton.font()
            font.setPointSize(16)
            font.setBold(True)
            holdButton.setFont(font)
            holdButtonPolicy = holdButton.sizePolicy()
            holdButtonPolicy.setHorizontalPolicy(QSizePolicy.MinimumExpanding)
            #holdButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
            holdButton.setCheckable(True)
            holdButton.clicked.connect(partial(self.onHoldButtonClick, idx=i))
            self.holdButtons.append(holdButton)
            self.grid.addWidget(holdButton, 3, i, QtCore.Qt.AlignVCenter)

        self.betUpButton = QPushButton("BET 1")
        self.betUpButton.setStyleSheet("background-color: #ffe73c;"
                                    "color: black;")
        font = self.betUpButton.font()
        font.setPointSize(16)
        font.setBold(True)
        self.betUpButton.setFont(font)
        self.betUpButton.clicked.connect(partial(self.onBetUpButtonClick))

        self.dealButton = QPushButton("DEAL")
        self.dealButton.setStyleSheet("background-color: #ffe73c;"
                                    "color: black;")
        font = self.dealButton.font()
        font.setPointSize(16)
        font.setBold(True)
        self.dealButton.setFont(font)
        self.dealButton.clicked.connect(partial(self.onDealButtonClick))

        self.creditsLabel = QLabel("Credits: "+str(self.game.credits))
        font = self.creditsLabel.font()
        font.setPointSize(16)
        self.creditsLabel.setFont(font)
        self.betLabel = QLabel("Bet: "+str(self.game.bet))
        font = self.betLabel.font()
        font.setPointSize(16)
        self.betLabel.setFont(font)

        # spacer label
        self.grid.addWidget(QLabel(""), 4, 0)

        self.grid.addWidget(self.betUpButton, 5, 0)
        self.grid.addWidget(self.creditsLabel, 5, 1)
        self.grid.addWidget(self.betLabel, 5, 3)
        self.grid.addWidget(self.dealButton, 5, 4)


        self.setLayout(self.grid)
        self.setWindowTitle("VIDEO POKER")
        self.setStyleSheet("color: #ffe73c;"
                        "background-color: #0000a0;"
                        "selection-color: #ffe73c;"
                        "selection-background-color: #0000a0;")
        #self.setGeometry(50,50,200,200)
        self.show()
        #self.showFullScreen()

    def onHoldButtonClick(self, checked, idx):
        print(checked) #<- only used if the button is checkable
        print('clicked')
        print("holdButton"+str(idx)+"Click")
        if self.game.phase != "hold":
            return
        if checked:
            self.game.add_hold(idx)
        else:
            self.game.remove_hold(idx)

    def onDealButtonClick(self, checked):
        print("dealButtonClick")
        for b in self.holdButtons:
            b.setChecked(False)
        if self.game.phase == "bet" and self.game.bet > 0:
            self.game.deck.reset()
            print(len(self.game.deck.cards))
            self.game.get_new_hand()
            score = self.game.hand.get_highest_score()
            for idx, l in enumerate(self.cardLabels):
                pixmap = QPixmap(self.game.hand.cards[idx].img_path)
                #self.im = pixmap.scaledToWidth(120)
                # im = pixmap.scaledToHeight(240)
                im = pixmap.scaled(240, 240, QtCore.Qt.KeepAspectRatio)
                l.setPixmap(im)
                playsound("assets/audio/click.mp3")
                time.sleep(0.2)
                l.update()
            if score:
                self.scoreLabel.setText(score.replace("_", " ").upper())
                self.scoreLabel.update()
                playsound("assets/audio/pay.mp3")
            self.game.change_phase("hold")
        elif self.game.phase == "hold":
            print(len(self.game.deck.cards))
            # show only new cards plus held cards
            # show score and update credits
            self.game.draw(self.game.hold_idxs)
            score = self.game.hand.get_highest_score()
            for idx, l in enumerate(self.cardLabels):
                if idx not in self.game.hold_idxs:
                    pixmap = QPixmap(self.game.hand.cards[idx].img_path)
                    #self.im = pixmap.scaledToWidth(120)
                    # im = pixmap.scaledToHeight(240)
                    im = pixmap.scaled(240, 240, QtCore.Qt.KeepAspectRatio)
                    l.setPixmap(im)
                    playsound("assets/audio/click.mp3")
                    time.sleep(0.2)
                    l.update()
            if score:
                self.scoreLabel.setText(score.upper().replace("_", " "))
                self.scoreLabel.update()
                if PAYTABLE[score] < 3:
                    playsound("assets/audio/pay2.mp3")
                elif PAYTABLE[score] >= 3 and PAYTABLE[score] < 10:
                    playsound("assets/audio/pay3.mp3")
                else:
                    playsound("assets/audio/pay4.mp3")

                winnings = PAYTABLE[score] * self.game.bet
                print(score+"! you win "+str(winnings)+" credits!")
                self.game.credits += winnings
            self.game.change_phase("bet")

        # refresh credits and bet label
        self.creditsLabel.setText("Credits: "+str(self.game.credits))
        self.betLabel.setText("Bet: "+str(self.game.bet))
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
                pixmap = QPixmap('assets/images/red_back.png')
                #self.im = pixmap.scaledToWidth(120)
                # im = pixmap.scaledToHeight(240)
                im = pixmap.scaled(240, 240, QtCore.Qt.KeepAspectRatio)
                l.setPixmap(im)
                l.update()
        self.game.add_bet(1)
        print(self.game.bet)
        print(self.game.credits)
        # refresh credits and bet label
        self.creditsLabel.setText("Credits: "+str(self.game.credits))
        self.betLabel.setText("Bet: "+str(self.game.bet))
        self.creditsLabel.update()
        self.betLabel.update()
        self.update()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GraphicalGame()
    sys.exit(app.exec_())
