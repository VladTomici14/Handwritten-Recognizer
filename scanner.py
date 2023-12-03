import cv2
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True)
ap.add_argument("-s", "--save", required=False, default=False, type=bool)
args = vars(ap.parse_args())

image = cv2.imread(args["image"])


def showImage(image, title, save_image=False):
    if save_image:
        cv2.imwrite(f"test/outputs/{title}.png", image)

    while True:
        cv2.imshow(title, image)

        if cv2.waitKey(1) == ord("q"):
            break


def preprocessImage(image):
    kernel = np.ones((5, 5), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=3)

    return image


def applyMask(image):
    mask = np.zeros(image.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    rectangle = (20, 20, image.shape[1]-20, image.shape[0]-20)

    cv2.grabCut(image, mask, rectangle, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
    image = image * mask2[:, :, np.newaxis]

    return image


image = preprocessImage(image)
image = applyMask(image)
cv2.imwrite("test/outputs/test.png", image)
