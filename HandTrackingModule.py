import cv2
import mediapipe as mp
import time


class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands,
                                         self.detection_con, self.track_con)
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None
        self.tip_ids = [4, 8, 12, 16, 20]
        self.lm_list = []

    def find_hands(self, img, draw=True):
        # Convert image to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Process frame and give results
        self.results = self.hands.process(img_rgb)
        # Check if hand(s) detected
        if self.results.multi_hand_landmarks:
            # Draws hand landmark points and their line connections
            for landmark in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, landmark, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_num=0, draw=True):
        # List tracks hand landmark id # and its center position
        self.lm_list = []
        # Check if hand(s) detected
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_num]

            # Loop through hand landmarks
            for id_num, lm in enumerate(my_hand.landmark):
                # Get height, width, and channels of image
                h, w, c = img.shape
                # Obtain center position of a hand landmark
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id_num, cx, cy])
                # Draw a circle representing a hand landmark
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return self.lm_list

    def fingers_up(self):
        # Check if hand(s) detected
        fingers = []
        if self.results.multi_hand_landmarks:
            # Thumb
            # Check if left or right hand
            if self.results.multi_handedness[0].classification[0].label == "Left":
                # Check if tip of thumb is on right or left to determine if open (1) or closed (0).
                if self.lm_list[self.tip_ids[0]][1] > self.lm_list[self.tip_ids[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if self.lm_list[self.tip_ids[0]][1] < self.lm_list[self.tip_ids[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Other 4 Fingers
            for finger_id in range(1, 5):
                if self.lm_list[self.tip_ids[finger_id]][2] < self.lm_list[self.tip_ids[finger_id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        return fingers


def main():
    prev_time = 0
    # Use webcam to capture video
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        # Obtain image frame from webcam video
        success, img = cap.read()
        # Update image with hand drawings
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        # Display fps
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        # Display image in window
        cv2.imshow("Image", img)
        # Display image for at least 1 ms
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
