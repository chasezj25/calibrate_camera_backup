import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pickle

CHECKER_WIDTH = .03658
CHECKER = (6,4)

cam_index = -1
def main():
    cap = None
    for i in range(10):
        cap = cv2.VideoCapture(i)
        try:
            if cap.isOpened():
                print(f"Camera found at index: {i}")
                cam_index = i
                break
        except:
            print("Exception ignored")
    if i == -1:
        print("No viable cameras found")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    count = 0
    print("Hit the space bar to take a picture and click q to finish taking pictures")
    while True:
        #print('.')
        ret, frame = cap.read()
        cv2.imshow('preview', frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        if key & 0xFF == ord(' '):
            print(f"Say cheese!\nPhotos so far: {count + 1}")
            #print(type(frame))
            image = Image.fromarray(frame)
            image.save(f"data/calib_img{count}.jpeg")
            count += 1
    cap.release()
    cv2.destroyAllWindows()
    if count == 0:
        print("No photos captured, returning")
        return
    K = np.zeros((3,3))
    for i in range(count):
        img = cv2.imread(f'data/calib_img{i}.jpeg')
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        flag_found, corners = cv2.findChessboardCorners(img_gray, CHECKER)

        criteria_subpix = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners_refined = cv2.cornerSubPix(img_gray, corners, (11,11), (-1,-1), criteria_subpix)

        obj_points = np.zeros( (CHECKER[0] * CHECKER[1], 1, 3 ), np.float32)
        for i in range(CHECKER[1]):
            for j in range(CHECKER[0]):
                obj_points[i*CHECKER[0]+j,0,:]=np.array([[j,i,0]])
        obj_points *= CHECKER_WIDTH

        err, k, dist_coeff, rvecs, tvecs = cv2.calibrateCamera([obj_points], [corners_refined], img_gray.shape[::-1], None, None)
        
        print(f"Stats from image {i}")
        print(f"Error: {err}")
        print(f"Calibration matrix K: \n{k}")
        print(f"Distance coeficient: {dist_coeff}\n\n")

        K += k
    K /= 1.0 * count
    
    with open("K-np-matrix.pkl", "wb") as f:
        try:
            pickle.dump(K, f)
            print("Stored the calibration matrix as \"K-np-matrix.pkl\"")
        except:
            print("Pickle error, returning")
            return
    ### Visual evaluation of success ###
    print("The following is still a work in progress\nImage may not appear correct, but the results are stored in \"visual_check.jpeg\"")
    R, _ = cv2.Rodrigues(rvecs[0])
    T = tvecs[0]

    M = K @ np.concatenate( (R, T) , axis=1)


    p_W = np.array([ [0,0,0,1], [CHECKER_WIDTH, 0, 0, 1] ]).T
    p_I = M @ p_W
    p_I = p_I[0:2,:]/p_I[2,:]
    p_I = p_I.astype(int)
    
    img_line = img.copy()
    cv2.line(img_line, (p_I[0,0], p_I[1,0]), (p_I[0,1], p_I[1,1]), (0,0,255), 2)

    p_W = np.array([ [0,0,0,1], [0, 0, -CHECKER_WIDTH, 1] ]).T
    p_I = M @ p_W
    p_I = p_I[0:2,:]/p_I[2,:]
    p_I = p_I.astype(int)

    cv2.line(img_line, (p_I[0,0], p_I[1,0]), (p_I[0,1], p_I[1,1]), (0,0,255), 2)

    p_W = np.array([ [0,0,0,1], [0, CHECKER_WIDTH, 0, 1] ]).T
    p_I = M @ p_W
    p_I = p_I[0:2,:]/p_I[2,:]
    p_I = p_I.astype(int)
    cv2.line(img_line, (p_I[0,0], p_I[1,0]), (p_I[0,1], p_I[1,1]), (0,0,255), 2)
    cv2_imshow(img_line)

    image = Image.fromarray(img_line)
    image.save(f"visual_check.jpeg")
def cv2_imshow(image):
# developed by Kanishke Gamagedara, udpated by MAE6292
    plt.figure(dpi=200)
    mode = len(np.shape(image))
    if mode==3:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    elif mode==2:
        plt.imshow(image, cmap='gray')
    else:
        print('Unsuported image size')
        raise
    plt.xticks([]), plt.yticks([])
    plt.axis('off')
if __name__ == '__main__':
    main()
