import random
import vlc
import winsound
import glob

from PyQt6.QtCore import Qt, QSize, QTimer, QEventLoop
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QIcon, QImage

from constructGUI import construct

##########
yoko = 4
tate = 2
##########

total_card = tate * yoko

plyaer_none = vlc.MediaListPlayer()
player_ok = vlc.MediaListPlayer()
player_finish = vlc.MediaListPlayer()

mediaList0 = vlc.MediaList(['./pic/dummy.wav'])
mediaList1 = vlc.MediaList(['./pic/ok.wav'])
mediaList2 = vlc.MediaList(['./pic/yattane.wav'])

plyaer_none.set_media_list(mediaList0)
player_ok.set_media_list(mediaList1)
player_finish.set_media_list(mediaList2)

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
        card_layout = QGridLayout()
        
        self.card_label =[QPushButton() for i in range(total_card)]
        
        for i in range(total_card):
            self.card_label[i].setObjectName(str(i))
            self.card_label[i].setFlat(True)   
            self.card_label[i].setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
            self.card_label[i].clicked.connect(self.buttonClicked)  
            card_layout.addWidget(self.card_label[i], i // yoko, i % yoko)
        ### main ###
        
        ### footer ###
        button_layout = QHBoxLayout()

        self.start_button = construct(QPushButton('start'), 'settings.yaml', 'button_1')
        self.start_button.clicked.connect(self.game_start)
        self.start_button.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        
        self.exit_button = construct(QPushButton('exit'), 'settings.yaml', 'button_1')
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        button_layout.addWidget(QLabel())
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.exit_button)
        button_layout.addWidget(QLabel())
        ### footer ###

        vbox = QVBoxLayout()
        vbox.addLayout(card_layout, 8)
        vbox.addLayout(button_layout, 1)

        self.setLayout(vbox)

        self.show()

    def exit(self):
        self.close()

    def game_start(self):

        if self.now_playing == True:
            return None

        plyaer_none.play()

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
            player_ok.play()
            if sum(self.button_enable) == 0:
                self.game_finish()
        else:
            winsound.MessageBeep()

            ### wait for 800msec ###
            loop = QEventLoop()
            QTimer.singleShot(800, loop.quit)
            loop.exec()

            self.button_enable[self.first_select] = True
            self.button_enable[self.second_select] = True
            self.set_image_into_button(self.img[0], self.card_label[self.first_select])
            self.set_image_into_button(self.img[0], self.card_label[self.second_select])

        self.first_select = -1
        self.second_select = -1

    def game_finish(self):
        
        player_finish.play()
        self.now_playing = False

    def set_image_into_button(self, image, button):
        w = button.width()
        h = button.height()
        img = QPixmap.fromImage(image.scaled(w-10, h-10, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        button.setIcon(QIcon(img))
        button.setIconSize(QSize(img.size()))

app = QApplication([])
ex =Window()
ex.showFullScreen()
app.exec()
