import cv2 as cv
import numpy as np
import os
import time
from windowCapture import WindowCapture
from vision import Vision
import pyautogui as pg
import math
import pygetwindow as gw
import keyboard
from harvestSeedAndCrops import harvestSeedAndCrops
from focus_window import focusWindow
wincap = WindowCapture()
wincap.list_window_names()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

     

def openInventory():
    ### open the inventory and put mouse on a casual item angle
    vision_invetory = Vision('inventoryAngle.png')

    #open the inventory
    print("apro l'invetario")
    pg.press('i')
    time.sleep(0.5)

    screenshot = pg.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_cv = cv.cvtColor(screenshot_np, cv.COLOR_RGB2BGR)

    best_match = vision_invetory.find_best_match(screenshot_cv, threshold=0.9)

    if best_match is not None:
        abs_pos = wincap.translate_to_screen_coords(best_match)
        pg.moveTo(abs_pos[0], abs_pos[1])
        print("inventario trovato!")
        return True
    else:
        print("inventario non trovato")
        return False
    
def getSeed(cropPath):
    vision_seed = Vision(cropPath,cv.TM_CCOEFF_NORMED)
    ###### enter the game #####
    focusWindow()
    ##### if open invetory is True so vision get the mouse on the invetory continue
    if openInventory():
        while True:
            screenshot = wincap.get_screenshot()
            best_match = vision_seed.find_best_match(screenshot, threshold=0.8)
            if best_match is not None:
                bstmtch = wincap.translate_to_screen_coords(best_match)
                pg.moveTo(bstmtch)
                pg.leftClick()
                pg.leftClick()
                time.sleep(0.5)
                pg.press("esc")
                break
            else:
                pg.scroll(-10)

def plantMenu():
    print("You must have seed in your inventory")
    print("*************************************")
    print("select the seed you want to plant")
    print("1.fern seed")
    print("**************************************")
    getSeed("dataset/seedsInventory/fernSeed.png")


def plant():
    plantMenu()
    count_plant= 0
    vision_freeSpace = Vision("dataset/freeSpaces/freeSpace1.png",cv.TM_CCOEFF_NORMED)
    while True:
        if keyboard.is_pressed('right ctrl'):
            break
        
        screenshot = wincap.get_screenshot()

        best_match = vision_freeSpace.find_best_match(screenshot,0.3)
        if best_match is not None:
            best_abs = wincap.translate_to_screen_coords(best_match)
            print("moving to" + str(best_abs))
            pg.moveTo(best_abs[0], best_abs[1])
            pg.leftClick()
            print(f"ho piantato {count_plant} piante fin'ora")
            count_plant += 1
            if count_plant == 100:
                break
        else:
            break


def antiAfk():
    count = 0
    focusWindow()
    time.sleep(1)
    screen_width, screen_height = pg.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    while True:
        pg.moveTo(center_x-75,center_y-50)
        print("moved")
        pg.click()
        pg.moveTo(center_x,center_y)
        time.sleep(3.5)
        pg.moveTo(center_x+90,center_y+75)
        pg.click()
        count +=1
        time.sleep(10)
        if count >= 55:
            break

harvestSeedAndCrops("dataset/seeds/nostrilWithSeed.png")