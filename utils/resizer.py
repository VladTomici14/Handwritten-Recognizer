import argparse
import cv2


class Resize:
    def __init__(self, args):
        self.target_height = args["height"]
        self.target_width = args["width"]

    def calculateHeight(self, target_width, image):
        return int((image.shape[0] * target_width) // image.shape[1])

    def calculateWidth(self, target_height, image):
        return int((image.shape[1] * target_height) // image.shape[0])

    def main(self):
        if self.target_width is None and self.target_height is not None:
            raise Exception("Please specify a size for the target")

        input_images = []
        for image in input_images:
            if self.target_height is None:
                # calculate width ratio for reach picture
                target_height = self.calculateHeight(self.target_width, image)
            if self.target_width is None:
                # calculate height ratio for reach picture
                target_width = self.calculateHeight(self.target_height, image)


if __name__ == "__main__":
    # ---------------- extracting the arguments for the target size ----------------
    ap = argparse.ArgumentParser()
    ap.add_argument("--height", required=False, type=int, help="target height for resizing")
    ap.add_argument("--width", required=False, type=int, help="target width for resizing")
    args = vars(ap.parse_args())

    resizer = Resize(args)
