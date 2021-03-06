import random
import winsound
import glob

import sys
from PyQt5.QtCore import Qt, QSize, QTimer, QEventLoop
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QImage, QFont

##########
tate = 4
yoko = 2
##########

total_card = tate * yoko

img_path_list = glob.glob('./pic/*.jpg')

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.image_id = []
        self.now_playing = False
        self.input_ready = False
        self.button_enable = []
        self.first_select = -1
        self.second_select = -1

    def initUI(self):

        self.img = [QImage(x) for x in img_path_list]

        ### main ###
        main = QFrame()
        main.setFrameStyle(QFrame.Box | QFrame.Plain)
        
        card_layout = QGridLayout()
        
        self.card_label =[QPushButton() for i in range(total_card)]
        
        for i in range(total_card):
            self.card_label[i].setObjectName(str(i))
            self.card_label[i].setFlat(True)
            self.card_label[i].setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.card_label[i].clicked.connect(self.buttonClicked)  
            card_layout.addWidget(self.card_label[i], i // tate, i % tate)
        main.setLayout(card_layout)
        ### main ###
        
        ### footer ###
        footer = QFrame()

        button_layout = QHBoxLayout()

        self.start_button = QPushButton('start')
        self.start_button.setFont(QFont("Times", 24, QFont.Bold))
        self.start_button.clicked.connect(self.game_start)
        self.start_button.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        
        self.exit_button = QPushButton('exit')
        self.exit_button.setFont(QFont("Times", 24, QFont.Bold))
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        button_layout.addWidget(QLabel())
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.exit_button)
        button_layout.addWidget(QLabel())

        footer.setLayout(button_layout)
        ### footer ###

        vbox = QVBoxLayout()
        vbox.addWidget(main, 6)
        vbox.addWidget(footer, 1)

        self.setLayout(vbox)

        self.show()

    def exit(self):
        self.close()

    def game_start(self):

        if self.now_playing == True:
            return None

        self.now_playing = True

        self.button_enable = [True] * total_card
        self.first_select = -1
        self.second_select = -1
        
        self.image_id = random.sample(range(1, len(img_path_list)), int(total_card/2)) * 2
        random.shuffle(self.image_id)

        for i in range(total_card):
            self.set_image_into_button(self.img[0], self.card_label[i])
        
        self.input_ready = True

    def buttonClicked(self):

        if self.input_ready == False:
            return None
        
        sender = self.sender()
        your_select = int(sender.objectName())
        
        if self.button_enable[your_select] == False:
            return None
        
        self.input_ready = False

        if self.first_select == -1:
            self.first_select = your_select
            self.button_enable[self.first_select] = False
            self.set_image_into_button(self.img[self.image_id[self.first_select]], self.card_label[self.first_select])
        else:
            self.second_select = your_select
            self.set_image_into_button(self.img[self.image_id[self.second_select]], self.card_label[self.second_select])

        if self.second_select != -1:
            self.judge()
        
        self.input_ready = True

    def judge(self):
        if self.image_id[self.first_select] == self.image_id[self.second_select]:
            self.button_enable[self.second_select] = False
            if sum(self.button_enable) == 0:
                self.game_finish()
        else:
            ### wait for 800msec ###
            loop = QEventLoop()
            QTimer.singleShot(800, loop.quit)
            loop.exec_()

            self.button_enable[self.first_select] = True
            self.button_enable[self.second_select] = True
            self.set_image_into_button(self.img[0], self.card_label[self.first_select])
            self.set_image_into_button(self.img[0], self.card_label[self.second_select])

        self.first_select = -1
        self.second_select = -1

    def game_finish(self):
        
        self.now_playing = False

    def set_image_into_button(self, image, button):
        w = button.width()
        h = button.height()
        img = QPixmap.fromImage(image.scaled(w-10, h-10, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        button.setIcon(QIcon(img))
        button.setIconSize(QSize(img.size()))

app = QApplication(sys.argv)
ex =Window()

ex.showFullScreen()
sys.exit(app.exec_())
