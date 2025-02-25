import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
def feature_matching():
    fileNames=glob.glob("uploads/*")

    img1 = cv2.imread(fileNames[0])
    img2 = cv2.imread(fileNames[1])

    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    akaze = cv2.AKAZE_create()
    kp1, des1 = akaze.detectAndCompute(img1, None)
    kp2, des2 = akaze.detectAndCompute(img2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    ratio = 0.75
    good = []
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good.append(m)
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    h, w = img2.shape[:2]
    img1_aligned = cv2.warpPerspective(img1, M, (w, h))

    diff = cv2.absdiff(img2, img1_aligned)
    cv2.imwrite("static/result.jpg", diff)

if __name__ == "__main__":
    feature_matching()