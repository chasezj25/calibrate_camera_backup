import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
WIDTH = 640
HEIGHT = 480
FILENANE = "output.avi"
cam_index = -1
def main():
    try:
        os.remove(FILENAME)
    except:
        pass
    cap = None
    for i in range(10):
        vid = cv2.VideoCapture(i)
        try:
            if vid.isOpened():
                print(f"Camera found at index: {i}")
                cam_index = i
                break
        except:
            print("Exception ignored")
    if i == -1:
        print("No viable cameras found")
        return
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('FILENAME', fourcc, 20.0, (WIDTH, HEIGHT))
    print("Type \'q\' to stop recording")
    while True:
        ret, frame = vid.read()
        cv2.imshow('frame', frame)
        frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
        out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    vid.release
    out.release
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
