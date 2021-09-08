import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap

from cards import Deck

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()

        deck = Deck()
        cards = deck.get_hand(5).cards

        for i,c in enumerate(cards):
            pixmap = QPixmap(c.img_path)
            #self.im = pixmap.scaledToWidth(120)
            im = pixmap.scaledToHeight(120)
            label = QLabel()
            label.setPixmap(im)

            self.grid.addWidget(label,1,i)

        self.setLayout(self.grid)

        self.grid.addWidget(QPushButton("HOLD"), 3, 0)
        self.grid.addWidget(QPushButton("HOLD"), 3, 1)
        self.grid.addWidget(QPushButton("HOLD"), 3, 2)
        self.grid.addWidget(QPushButton("HOLD"), 3, 3)
        self.grid.addWidget(QPushButton("HOLD"), 3, 4)

        self.grid.addWidget(QPushButton("DEAL"), 4, 2)


        self.setLayout(self.grid)
        self.setWindowTitle("VIDEO POKER")
        self.setGeometry(50,50,200,200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
