from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QSizePolicy, QSpacerItem, QLabel)
from PyQt5.QtCore import QSize, QUrl, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap, QPalette, QBrush
import argparse
from config import start_directory
import sys
import os

class SoundboardApp(QWidget):
    def __init__(self, fullscreen=False):
        super().__init__()
        self.title = 'Gachiboard'
        self.left = 100
        self.top = 100
        # We're designing this to the standard issue 3.5" touch displays
        self.width = 320
        self.height = 480
        if fullscreen:
            self.showFullScreen()
        else:
            self.setFixedSize(320, 480)
        # Fixed size for buttons
        self.buttonSize = QSize(100, 100)  
        self.soundboards = {}
        self.autoCreateDictionary()
        if len(self.soundboards) == 0:
            sys.exit('No sounds loaded. Make sure that the sounds -subfolder has soundboard in there with sounds')
        self.currentPage = 0
        self.currentBoard = list(self.soundboards.keys())[0]
        self.player = QMediaPlayer()
        self.initUI()

    def autoCreateDictionary(self):
        folder_files = self.enumerate_soundboard_files(start_directory)
        for folder, data in folder_files.items():
            soundboard = folder
            label_file_pairs = []
            background = data['background']
            for filename in data['sounds']:
                # Label creation
                base = os.path.basename(filename)
                filename_without_extension = os.path.splitext(base)[0]
                label_name = filename_without_extension.replace('_', ' ').capitalize()
                label_file_pairs.append((label_name, filename))
            # Got everything, insert now the entry and don't interract with empty dirs:
            if len(data['sounds']) != 0:
                self.add_entry(self.soundboards, soundboard, label_file_pairs, background)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # So that the view doesn't jump around all the time
        self.setFixedSize(320, 480)
        self.updateBackground()
        
        # Main layout creation
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(10)
        # So that there isn't weirdly large margins
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        
        # Soundboard list selector creation
        self.chooseBoardCombo = QComboBox(self)
        self.chooseBoardCombo.addItems(list(self.soundboards.keys()))
        self.chooseBoardCombo.currentIndexChanged.connect(self.chooseSoundboard)
        self.mainLayout.addWidget(self.chooseBoardCombo)
        
        # Spacer to push everything up
        self.mainLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Sound buttons
        self.soundButtonsLayout = QGridLayout()
        self.soundButtonsLayout.setSpacing(10)
        self.soundButtons = []
        self.soundLabels = []
        for i in range(6):
            button = QPushButton('', self)
            button.clicked.connect(self.playSound)
            button.hide() 
            button.setFixedSize(self.buttonSize)
            buttonLayout = QVBoxLayout() 
            button.setLayout(buttonLayout)

            # Initialize the label with empty text, these are inside the buttons
            label = QLabel('')  
            label.setAlignment(Qt.AlignCenter)
            label.setWordWrap(True) 
            # Add label to the button
            buttonLayout.addWidget(label)
            self.soundButtons.append(button)
            self.soundLabels.append(label)
            row = i // 2 
            col = i % 2
            self.soundButtonsLayout.addWidget(button, row, col)
        
        
        self.mainLayout.addLayout(self.soundButtonsLayout)
        
        # To keep things at bottom
        self.mainLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Nav
        self.navigationLayout = QHBoxLayout()
        self.navigationLayout.setSpacing(10)
        self.previousPageButton = QPushButton('Previous', self)
        self.previousPageButton.clicked.connect(self.goToPreviousPage)
        self.navigationLayout.addWidget(self.previousPageButton)
        
        self.nextPageButton = QPushButton('Next', self)
        self.nextPageButton.clicked.connect(self.goToNextPage)
        self.navigationLayout.addWidget(self.nextPageButton)
        self.mainLayout.addLayout(self.navigationLayout)

        self.setLayout(self.mainLayout)
        self.loadSounds() 
        self.show()

    def add_entry(self, dictionary, name, sounds, background):
        dictionary[name] = {
            'sounds': sounds,
            'background': background
        }

    def enumerate_soundboard_files(self, start_dir):
        folder_data = {}
        start_dir = os.path.abspath(start_dir)

        for root, dirs, files in os.walk(start_dir):
            sound_files = []
            # TODO set a default one?
            background_img = None
            for file in files:
                if file.endswith(('.wav', '.mp3')):
                    full_path = os.path.join(root, file)
                    filename = os.path.basename(full_path)
                    #mp3_files.append(filename)
                    sound_files.append(full_path)
                elif file.lower() == 'background.jpg':
                    background_img = os.path.join(root, file)


            if sound_files or background_img:
                # Get a relative path for the folder name from the start_dir
                relative_folder_path = os.path.relpath(root, start_dir)
                folder_data[relative_folder_path] = {'sounds': sound_files, 'background': background_img}

        return folder_data

    def updateBackground(self):
        backgroundPath = self.soundboards[self.currentBoard]['background']
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap(backgroundPath)))
        self.setPalette(palette)
    
    def goToPreviousPage(self):
        if self.currentPage > 0:
            self.currentPage -= 1
            self.loadSounds()
    
    def goToNextPage(self):
        totalSounds = len(self.soundboards[self.currentBoard]['sounds'])
        if (self.currentPage + 1) * 6 < totalSounds:
            self.currentPage += 1
            self.loadSounds()
    
    def chooseSoundboard(self, index):
        self.currentBoard = self.chooseBoardCombo.itemText(index)
        self.currentPage = 0
        self.updateBackground()
        self.loadSounds()
    
    def loadSounds(self):
        startIdx = self.currentPage * 6
        endIdx = startIdx + 6
        sounds = self.soundboards[self.currentBoard]['sounds'][startIdx:endIdx]
        
        for i, button in enumerate(self.soundButtons):
            if i < len(sounds):
                # Sound name
                self.soundLabels[i].setText(sounds[i][0])
                button.show()
            # Checking if button needs temporary hiding due to count
            else:
                button.hide()
        
        # Checking if button needs enabling
        totalSounds = len(self.soundboards[self.currentBoard]['sounds'])
        self.nextPageButton.setEnabled(endIdx < totalSounds)

    def playSound(self):
        sender = self.sender()
        buttonIndex = self.soundButtons.index(sender)
        buttonText = self.soundLabels[buttonIndex].text()
        soundPath = [s[1] for s in self.soundboards[self.currentBoard]['sounds'] if s[0] == buttonText]
        if soundPath:
            sound_path = soundPath[0]
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(sound_path)))
            self.player.play()



if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--fullscreen", help="Launch app in fullscreen mode", action="store_true")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    ex = SoundboardApp(fullscreen=args.fullscreen)
    sys.exit(app.exec_())
