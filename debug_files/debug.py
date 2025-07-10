import cv2 as cv
from vision import Vision
from windowCapture import WindowCapture
import numpy as np

def draw_points(image, points, color=(0, 255, 0), radius=10):
    for point in points:
        cv.circle(image, (int(point[0]), int(point[1])), radius, color, 2)
    return image

def main():
    wincap = WindowCapture()
    screenshot = wincap.get_screenshot()
    
    vision = Vision('1.png')
    relative_points = vision.find(screenshot, 0.239)
    absolute_points = wincap.translate_to_screen_coords(relative_points)

    print("=== PUNTI TROVATI ===")
    for i, (rel, abs_) in enumerate(zip(relative_points, absolute_points)):
        print(f"[{i}] Relativo: {rel} | Assoluto: {abs_}")

    debug_img = draw_points(screenshot.copy(), relative_points, color=(255, 0, 0))
    cv.imshow("DEBUG Template Matches", debug_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
