import datetime
import cv2
import numpy as np
import matplotlib.pyplot as plt

def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 5000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest, max_area


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew


def drawRectangle(img, biggest, thickness):
    cv2.line(img, (biggest[0][0][0], biggest[0][0][1]), (biggest[1][0][0], biggest[1][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[0][0][0], biggest[0][0][1]), (biggest[2][0][0], biggest[2][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[3][0][0], biggest[3][0][1]), (biggest[2][0][0], biggest[2][0][1]), (0, 255, 0), thickness)
    cv2.line(img, (biggest[3][0][0], biggest[3][0][1]), (biggest[1][0][0], biggest[1][0][1]), (0, 255, 0), thickness)

    return img


def nothing(x):
    pass


def initializeTrackbacks(initialTrackbarVals=0):
    cv2.namedWindow("trackbars")
    cv2.resizeWindow("trackbars", 360, 240)
    cv2.createTrackbar("threshold1", "trackbars", 200, 255, nothing)
    cv2.createTrackbar("threshold2", "trackbars", 200, 255, nothing)


def valTrackbars():
    threshold1 = cv2.getTrackbarPos("threshold1", "trackbars")
    threshold2 = cv2.getTrackbarPos("threshold2", "trackbars")
    return threshold1, threshold2


def plottingResults(results, titles):
    figure = plt.figure(figsize=(15, 7))

    for i in range(0, 4):
        results[i] = cv2.cvtColor(results[i], cv2.COLOR_BGR2RGB)

        figure.add_subplot(1, 4, i+1).set_title(str(titles[i]))
        plt.imshow(results[i])

    figure.savefig(str(f"test/results/results-{datetime.date.today()}-{titles[0]}"))






