# Gachiboard

This is a Python + QT based soundboard software intended to be used with 3.5" touchscreen displays e.g. with Raspberry Pi but it's size should be still enough for desktop use.


## Features

- Automatical discovery of files in the defined directory
- Automatical sorting of files and labeling their buttons
- Background is set for each soundboard automatically

## Usage

You should run this in a virtual environment and install the required requirements from the requirements.txt regarding PyQT5.

Then, you should be ready to drop some soundboard files under the 'sounds' folder in their own directory, with the following structure:

- `/gachiboard`  _Gachiboard root_
    - `sounds` _Sounds directory_
        - `/Example board`  _A Soundboard called 'Example board'_
            - `background.jpg`  _Background image for the soundboard_
            - `Example_sound.mp3`  _Sound file_

As you can see, the Gachiboard accepts mp3 files in a directory which will result to be the soundboard's name, meanwhile the filenames under there will be used to label buttons of the soundboard. `In the filenames, underscores will be turned into spaces.` You can also set a background image of 320x480 px resolution as a `background.jpg`. Once you're ready, you can run the Gachiboard from the virtual environment and it should automatically create you a layout with list of boards based on the folder structure.