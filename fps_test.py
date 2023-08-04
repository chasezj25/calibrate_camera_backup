import numpy as np
import cv2
import time
def main():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Could not open the camera")
        return
    start_time = time.time()
    span = None
    count = 0
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while True:
        count += 1
        ret, frame = camera.read()
        cv2.imshow('preview', frame)
        span = time.time() - start_time
        if span  >= 60:
            break
    print(f"The average fps was {count / span}") 
    cv2.destroyAllWindows()

    span = None
    start_time = time.time()
    while True:
        count += 1
        ret, frame = camera.read()
        span = time.time() - start_time
        if span  >= 60:
            break
    print(f"The average fps without Visual output {count / span}")
    camera.release()

if __name__ == "__main__":
    main()
