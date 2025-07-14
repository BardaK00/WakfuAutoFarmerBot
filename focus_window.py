import cv2 as cv
import numpy as np
import os
import time
from windowCapture import WindowCapture
from vision import Vision
import pyautogui as pg

import pygetwindow as gw



wincap = WindowCapture()
wincap.list_window_names()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def focusWindow():
    vision_window = Vision('icon.png', cv.TM_CCOEFF_NORMED)

    # Screenshot con pyautogui e conversione per OpenCV
    screenshot = pg.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_cv = cv.cvtColor(screenshot_np, cv.COLOR_RGB2BGR)

    best_match = vision_window.find_best_match(screenshot_cv, threshold=0.8)

    if best_match is not None:
        abs_pos = wincap.translate_to_screen_coords(best_match)
        pg.moveTo(abs_pos[0], abs_pos[1])
        pg.click()  # click sinistro
        time.sleep(1)
        print("✅ Finestra trovata e cliccata.")
    else:
        print("❌ Finestra non trovata o gioco non aperto, riprovare.")