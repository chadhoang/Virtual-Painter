# Virtual Painter
## About 
Virtual Painter is a python application that allows you to make illustrations by simply using your computer's camera and your hands. This application primarily uses OpenCV to accomplish this, which is an open source computer vision library.

## Setup
To use the application, please download the zip file, and unzip the file onto your device as is. The program can be run by simply entering the `Virtual-Painter-main` directory, then entering 
```
python VirtualPainter.py
```
It is also important to note that the application uses the following python packages, so please make sure they are installed into your device prior to running the program:
- mediapipe (link: https://google.github.io/mediapipe/getting_started/install.html)
- numpy (link: https://numpy.org/install/)
- OpenCV (link: https://pypi.org/project/opencv-python/)

The following packages can be easily installed onto your device using `pip`.
```
pip install mediapipe
```
```
pip install numpy
```
```
pip install opencv-python
```

(**Note**: The application requires access to your computer's webcam, so please be sure you are able to authorize your device's security settings to allow for camera use.)

## How to use
- Allow your hand to be displayed clearly to your camera. Keep your hand at an optimal distance from the camera. The program will display visual indicators that trace the shape of your hand when it is correctly recognized.
- DRAW MODE - This mode is triggered when stick only your **index finger** up. A circle following the tip of your index finger will help indicate that this mode is being used. This mode will allow you to draw by moving your index finger.
- SELECTION MODE - This mode is triggered when only your **index finger and middle finger** are lifted up. A rectangle will be created around these two fingers to indicate that this mode is being used. This mode allows for you to select from the many available options located on the sides of the program window, or also pause from drawing onto the image.
- PAINT option - Represented by the palette icon at top header of the program window, selecting this option allows you to paint onto the image.
- ERASE option - Represented by the eraser icon at the top header of the program window, this allows your drawing finger to be used as an eraser to remove parts of your drawing the you hover the eraser over.
- CLEAR option - Seen on the top right corner of the program window, selecting this option removes all of your previous drawings, resulting back to an original clear image.
- Left Tab - The grey tab on the left allows you to decrease red, green, blue, and brush thickness values.
- Right Tab - The grey tab on the right allows you to increase red, green, blue, and brush thickness values.
- END/EXIT PROGRAM - The program can be ended by selecting the top left corner of the program window, where the program's name "Virtual Painter" and its logos are located.

## Lessons Learned
I learned much about the OpenCV library, and of the many functionalities possible through this library. I was introduced to how the library stored data values representing images, and how to access these values to use for this program. Learning how to use a new library is always a challenge, but at the end, I was able to understand what each line of code accomplishes in my program, and how to accomplish larger objectives through combining various functionalities available within the library, such as how I was able to detect that only an index finger was raised to indicate to the program to begin drawing. 

This was also a great project to help me practice and improve my design choices. I chose to add functionalities to the program that went further then simply drawing onto an image, such as the ability to instantly reset the image, along with the ability to adjust the brush color and thickness. These features help to greatly expand the user's potential experience with the program, and to be able to implement the features without causing much other obstruction to the core functionalities of the program was a challenge that I felt I completed successfully. Take for example how I implemented the left and right tabs to adjust brush color and thickness. I sized these tabs so that they do not obstruct too much of the user's available drawing space, while also keeping the options raised in height so that the hand may be able to make selections onto them without going out of range of the camera's ability to detect the hand.

Overall, this project was a great exercise in my ability to work with new libraries and improve my design abilities, and I look forward to what I can make in the future with the knowledge that I gained from working on the project.
