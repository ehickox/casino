import sys, time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from functools import partial
from cards import Deck
from game import Game
from playsound import playsound

class GraphicalGame(QWidget):

    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()

        self.game = Game()
        self.cardLabels = []

        for i in range(0, 5):
            pixmap = QPixmap('assets/images/red_back.png')
            #self.im = pixmap.scaledToWidth(120)
            im = pixmap.scaledToHeight(240)
            label = QLabel()
            label.setPixmap(im)
            self.cardLabels.append(label)

            self.grid.addWidget(label,1,i)

        self.setLayout(self.grid)

        self.holdButton0 = QPushButton("HOLD")
        self.holdButton0.clicked.connect(partial(self.onHoldButtonClick, idx=0))
        self.holdButton1 = QPushButton("HOLD")
        self.holdButton1.clicked.connect(partial(self.onHoldButtonClick, idx=1))
        self.holdButton2 = QPushButton("HOLD")
        self.holdButton2.clicked.connect(partial(self.onHoldButtonClick, idx=2))
        self.holdButton3 = QPushButton("HOLD")
        self.holdButton3.clicked.connect(partial(self.onHoldButtonClick, idx=3))
        self.holdButton4 = QPushButton("HOLD")
        self.holdButton4.clicked.connect(partial(self.onHoldButtonClick, idx=4))

        self.grid.addWidget(self.holdButton0, 3, 0)
        self.grid.addWidget(self.holdButton1, 3, 1)
        self.grid.addWidget(self.holdButton2, 3, 2)
        self.grid.addWidget(self.holdButton3, 3, 3)
        self.grid.addWidget(self.holdButton4, 3, 4)

        self.betUpButton = QPushButton("BET 1")
        self.betUpButton.clicked.connect(partial(self.onBetUpButtonClick))
        self.dealButton = QPushButton("DEAL")
        self.dealButton.clicked.connect(partial(self.onDealButtonClick))

        self.creditsLabel = QLabel("Credits: "+str(self.game.credits))
        self.betLabel = QLabel("Bet: "+str(self.game.bet))

        self.grid.addWidget(self.betUpButton, 4, 0)
        self.grid.addWidget(self.creditsLabel, 4, 1)
        self.grid.addWidget(self.betLabel, 4, 3)
        self.grid.addWidget(self.dealButton, 4, 4)


        self.setLayout(self.grid)
        self.setWindowTitle("VIDEO POKER")
        self.setGeometry(50,50,200,200)
        self.show()

    def onHoldButtonClick(self, checked, idx):
        print(checked) #<- only used if the button is checkeable
        print('clicked')
        print("holdButton"+str(idx)+"Click")
        if self.game.phase != "hold":
            return

    def onDealButtonClick(self, checked):
        print("dealButtonClick")
        if self.game.phase == "bet" and self.game.bet > 0:
            self.game.get_new_hand()
            for idx, l in enumerate(self.cardLabels):
                playsound("assets/audio/click.mp3")
                pixmap = QPixmap(self.game.hand.cards[idx].img_path)
                #self.im = pixmap.scaledToWidth(120)
                im = pixmap.scaledToHeight(240)
                l.setPixmap(im)
                l.update()
                time.sleep(0.08)

            self.game.change_phase("hold")
        elif self.game.phase == "hold":
            # show only new cards plus held cards
            pass



    def onBetUpButtonClick(self, checked):
        print("betUpButtonClick")
        if self.game.phase != "bet":
            return
        self.game.add_bet(1)
        print(self.game.bet)
        print(self.game.credits)
        # refresh credits and bet label
        self.creditsLabel.setText("Credits: "+str(self.game.credits))
        self.betLabel.setText("Bet: "+str(self.game.bet))
        self.creditsLabel.update()
        self.betLabel.update()
        self.update()


    def play_hand(self):
        self.game.deck.reset()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GraphicalGame()
    #while True:
    #    ex.play_hand()
    #    app.processEvents()

    sys.exit(app.exec_())
