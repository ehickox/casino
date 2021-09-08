import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap

from cards import Deck
from game import Game

class GraphicalGame(QWidget):

    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()

        self.game = Game()

        for i in range(0, 5):
            pixmap = QPixmap('assets/images/red_back.png')
            #self.im = pixmap.scaledToWidth(120)
            im = pixmap.scaledToHeight(240)
            label = QLabel()
            label.setPixmap(im)

            self.grid.addWidget(label,1,i)

        self.setLayout(self.grid)

        self.grid.addWidget(QPushButton("HOLD"), 3, 0)
        self.grid.addWidget(QPushButton("HOLD"), 3, 1)
        self.grid.addWidget(QPushButton("HOLD"), 3, 2)
        self.grid.addWidget(QPushButton("HOLD"), 3, 3)
        self.grid.addWidget(QPushButton("HOLD"), 3, 4)

        self.grid.addWidget(QPushButton("BET 1"), 4, 0)
        self.grid.addWidget(QLabel("Credits: "+str(self.game.credits)), 4, 1)
        self.grid.addWidget(QLabel("Bet: "), 4, 3)
        self.grid.addWidget(QPushButton("DEAL"), 4, 4)


        self.setLayout(self.grid)
        self.setWindowTitle("VIDEO POKER")
        self.setGeometry(50,50,200,200)
        self.show()

    def play_hand(self):
        self.game.deck.reset()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GraphicalGame()
    while True:
        ex.play_hand()
        app.processEvents()
    sys.exit(app.exec_())
