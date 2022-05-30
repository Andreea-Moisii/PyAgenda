import cv2
import pyautogui


class VideoManager:
    quitFlag = False

    def start(self):
        print("Starting video capture")
        face_cascade = cv2.CascadeClassifier('video/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('video/haarcascade_eye.xml')

        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        # get screen size
        screen_width, screen_height = pyautogui.size()
        # get mouse position
        last_x, last_y = pyautogui.position()

        counter = 0
        self.quitFlag = True
        while self.quitFlag:
            ret, img = cap.read()

            # mirror image
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # cv2.rectangle(img, (50, 50), (590, 430), (255, 0, 0), 3)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x + int(w / 2), y + int(h / 2)), (x + int(w / 2), y + int(h / 2)), (0, 255, 0), 3)

                # get center of face
                center_x = x + int(w / 2)
                center_y = y + int(h / 2)

                # scale the center of face to the center of screen
                center_x = int(center_x * screen_width / 640)
                center_y = int(center_y * screen_height / 480)

                if abs(center_x - last_x) > 10 or abs(center_y - last_y) > 10:
                    # move global mouse to the center of face
                    pyautogui.moveTo(center_x, center_y)

                    # save mouse position
                    last_x = center_x
                    last_y = center_y

                    counter = 0
                else:
                    counter += 1
                    if counter > 10:
                        pyautogui.click()
                        counter = 0

            cv2.imshow('img', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        print("Stopping video capture")
        cap.release()
        cv2.destroyAllWindows()


