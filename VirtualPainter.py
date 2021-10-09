# VirtualPainter.py

# Import
import cv2
import numpy as np
import os
import HandTrackingModule as htm

# Constants
WINDOW_LENGTH = 720
WINDOW_WIDTH = 1280
HEADER_LENGTH = 125
BLACK = (0, 0, 0)
TAB_WIDTH = 80


def main():
    # Import header images
    my_list = os.listdir("Header")
    overlay_list = []
    for imPath in my_list:
        overlay_list.append(cv2.imread(f'{"Header"}/{imPath}'))

    # Default header image
    header = overlay_list[11]

    # Default side-tabs
    left_tab = overlay_list[14]
    right_tab = overlay_list[0]

    # Use webcam to display video in 1280x720 window
    cap = cv2.VideoCapture(0)
    cap.set(3, WINDOW_WIDTH)
    cap.set(4, WINDOW_LENGTH)

    # Set HandTrackingModule object variable
    detector = htm.HandDetector(detection_con=0.85)
    # Image canvas represents image that we draw on
    img_canvas = np.zeros((WINDOW_LENGTH, WINDOW_WIDTH, 3), np.uint8)
    # Set previous x and y coordinates of drawing finger to start position
    xp, yp = 0, 0
    # Set brush paint color and its thickness
    blue, green, red = 128, 128, 128
    brush_thickness = 15
    running = True
    clear = False
    draw_color = (blue, green, red)
    while running:
        # 1. Import image
        success, img = cap.read()
        # Flip image
        img = cv2.flip(img, 1)
        # 2. Find Hand Landmarks
        # Detect hand(s)
        img = detector.find_hands(img)
        # Obtain hand landmark info
        lm_list = detector.find_position(img, draw=False)
        # Check if gained hand info (hand detected)
        if len(lm_list) != 0:
            # Tip of index finger
            x1, y1 = lm_list[8][1:]
            # Tip of middle finger
            x2, y2 = lm_list[12][1:]
            # 3. Check which fingers are up
            fingers = detector.fingers_up()
            # 4. If Selection mode (index and middle fingers up)
            if fingers[1] and fingers[2]:
                # Reset previous x and y to start position
                xp, yp = 0, 0
                # Check for clicking header
                if y1 < HEADER_LENGTH:
                    # CLEAR option
                    if 1050 < x1 < WINDOW_WIDTH:
                        header = overlay_list[4]
                        clear = True
                    # DRAW option
                    elif 580 < x1 < 730:
                        header = overlay_list[5]
                        draw_color = (blue, green, red)
                    # ERASE option
                    elif 780 < x1 < 990:
                        header = overlay_list[9]
                        draw_color = BLACK
                    # EXIT option
                    elif x1 < HEADER_LENGTH:
                        running = False
                # Check for clicking left tab
                elif x1 < HEADER_LENGTH:
                    # - red
                    if 210 < y1 < 260:
                        if red > 0:
                            red -= 1
                        left_tab = overlay_list[8]
                    # - green
                    elif 290 < y1 < 340:
                        if green > 0:
                            green -= 1
                        left_tab = overlay_list[7]
                    # - blue
                    elif 380 < y1 < 420:
                        if blue > 0:
                            blue -= 1
                        left_tab = overlay_list[10]
                    # - thickness
                    elif 450 < y1 < 510:
                        if brush_thickness > 1:
                            brush_thickness -= 1
                        left_tab = overlay_list[13]
                    draw_color = (blue, green, red)
                # Check for clicking right tab
                elif x1 > WINDOW_WIDTH - HEADER_LENGTH:
                    # + red
                    if 210 < y1 < 260:
                        if red < 255:
                            red += 1
                        right_tab = overlay_list[12]
                    elif 290 < y1 < 340:
                        if green < 255:
                            green += 1
                        right_tab = overlay_list[6]
                    elif 380 < y1 < 420:
                        if blue < 255:
                            blue += 1
                        right_tab = overlay_list[1]
                    # + thickness
                    elif 450 < y1 < 510:
                        if brush_thickness < 255:
                            brush_thickness += 1
                        right_tab = overlay_list[2]
                    draw_color = (blue, green, red)
                # Reset header if finger not in range of clicking an option in header
                else:
                    header = overlay_list[11]
                    left_tab = overlay_list[14]
                    right_tab = overlay_list[0]
                # Draw a rectangle for selection mode's cursor
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), draw_color, cv2.FILLED)

            # 5. If Drawing mode (index finger up)
            if fingers[1] and not fingers[2]:
                # Draw a circle for drawing mode's cursor
                cv2.circle(img, (x1, y1), 15, draw_color, cv2.FILLED)

                # If previous x and y are at start position, update it immediately
                # to prevent glitch of drawing a line from top-left corner to drawing finger
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                # Draw on the image canvas
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, brush_thickness)
                # Update previous x and y
                xp, yp = x1, y1

        # Convert drawing image to create grey image
        img_grey = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
        # Create image inverse of grey image
        _, img_inv = cv2.threshold(img_grey, 50, 255, cv2.THRESH_BINARY_INV)
        # Convert inverse grey image to color
        img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
        # Reset canvas if CLEAR option selected
        if clear:
            img_canvas = np.zeros((WINDOW_LENGTH, WINDOW_WIDTH, 3), np.uint8)
        # Loads image
        img = cv2.bitwise_and(img, img_inv)
        # Loads drawing
        img = cv2.bitwise_or(img, img_canvas)

        # Set the header image (1280x125)
        img[0:HEADER_LENGTH, 0:WINDOW_WIDTH] = header
        # Set side tabs (125x595)
        img[HEADER_LENGTH:, 0:TAB_WIDTH] = left_tab
        img[HEADER_LENGTH:, WINDOW_WIDTH-TAB_WIDTH:] = right_tab
        # Display image onto new window
        cv2.putText(img, "Color: (R=" + str(red) + ", G=" + str(green) + ", B=" + str(blue) + ")",
                    (350, 50), cv2.FONT_HERSHEY_PLAIN, 1, BLACK, 1)
        cv2.putText(img, "Thickness: " + str(brush_thickness),
                    (350, 80), cv2.FONT_HERSHEY_PLAIN, 1, BLACK, 1)
        cv2.imshow("Virtual Painter", img)
        # Reset CLEAR option
        clear = False
        # Collect events until released
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
