import cv2
import numpy as np
import utils
import argparse

class Scanner:
    def __init__(self):
        pass

    def preprocessImage(self, input_image):
        """
        Preparing the input image by applying a gray filter and blurring the image.
            :param input_image: input image source
            :return: image with all the filters applied
        """
        grayscale = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(grayscale, (5, 5), 1)

        return image

    def applyMask(self, input_image):
        """
        Applying the mask filter on the image.
            :param input_image:
            :return: masked filter
        """

        thresh = (255, 255)
        image_threshold = cv2.Canny(input_image, thresh[0], thresh[1])
        kernel = np.ones((5, 5))
        dilated = cv2.dilate(image_threshold, kernel, iterations=2)
        threshold_mask = cv2.erode(dilated, kernel, iterations=1)

        return threshold_mask

    def getEdges(self, input_mask):
        """
        Getting the edges of the mask.
            :param image:
            :param img:
        :return:
        """
        contours, hierarchy = cv2.findContours(input_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:0]

        return contours

    def drawEdges(self, edges, input_image, color=(0, 255, 0)):
        """
        Drawing the contours on image
            :param edges: the contours
            :param input_image: the image that we will draw on
            :param color: color for the contours drawing
        :return: the input image with all the contours drawn on it
        """
        cv2.drawContours(input_image, contours, 2, color, 10)

        return input_image

    def drawContours(self, input_image, contours):
        cv2.drawContours(input_image, contours, -1, (0, 255, 0), 20)
        image_big_contour = utils.drawRectangle(input_image, contours, 2)

        return image_big_contour

    def changePerspectiveToScan(self, biggest_contour, input_image):
        """
        Morphing from image to scan.
            :param biggest_contour: detecting the biggest contour
            :param input_image:
        :return:
        """
        pts1 = np.float32(biggest_contour)
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        image_warp_colored = cv2.warpPerspective(input_image, matrix, (width, height))

        return image_warp_colored

    def removeBorders(self, scan):
        # --------- fine-tuning the resulted scan ---------
        image_warp_colored = scan[20:scan.shape[0] - 20, 20:scan.shape[1] - 20]
        image_warp_colored = cv2.resize(image_warp_colored, (width, height))

        return image_warp_colored

    def processOutputScan(self, scan):
        # --------- applying last filters for the output ---------
        image_warp_gray = cv2.cvtColor(scan, cv2.COLOR_BGR2GRAY)
        image_adaptive_threshold = cv2.adaptiveThreshold(image_warp_gray, 255, 1, 1, 7, 2)
        image_adaptive_threshold = cv2.bitwise_not(image_adaptive_threshold)
        output_scan = cv2.medianBlur(image_adaptive_threshold, 3)

        return output_scan

    def returnScan(self, image):
        processed_image = self.preprocessImage(image)

        # -------- applying the mask --------
        mask = self.applyMask(processed_image)

        # -------- finding the contours --------
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # -------- making the scan --------
        biggest, maxArea = utils.biggestContour(contours)
        if biggest.size != 0:
            biggest = utils.reorder(biggest)

            self.drawContours(detected_scan, biggest)
            scan = self.changePerspectiveToScan(biggest, image)
            scan = self.removeBorders(scan)
            processed_output = self.processOutputScan(scan)

            return processed_output
    
        else:
            error_image = np.zeros_like(image)
            cv2.putText(error_image, str("lol nu merge"), (image.shape[1] // 2, image.shape[0] // 2 - 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)

            print("vai mama")

            return error_image


if __name__ == "__main__":
    # -------- argparsing the input image --------
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="input image")
    args = vars(ap.parse_args())

    scanner = Scanner()

    # -------- loading the image --------
    image_path = args["image"]
    input_path = f"test/{image_path}"
    image = cv2.imread(input_path)
    detected_scan = image.copy()
    original_image = image.copy()
    (height, width) = image.shape[:2]

    final_output = scanner.returnScan(image)
    cv2.imwrite("final.png", final_output)



