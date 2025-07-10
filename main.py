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


wincap = WindowCapture()
wincap.list_window_names()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def checkCap():
    vision_cap = Vision("cap.png",cv.TM_CCOEFF_NORMED)
    while True:
        if keyboard.is_pressed('right ctrl'):
            break
        
        screenshot = wincap.get_screenshot()
        best_match = vision_cap.find_best_match(screenshot,0.8)
        if best_match is not None:
            pg.press('space')
            time.sleep(0.5)
            pg.press('del')
            time.sleep(1)
            pg.press('enter')
            time.sleep(3)
            pg.press('esc')
            time.sleep(0.5)
            break
        else:
            break
            
def focus_window():
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

def harvestCrop(cropPath):
    vision_button = Vision('dataset/buttons/getCrops.png', cv.TM_CCOEFF_NORMED)
    vision_crop = Vision(cropPath)
    while True:
        screenshot = wincap.get_screenshot()
        best_match = vision_crop.find_best_match(screenshot, threshold=0.21)

        if best_match is not None:
            best_abs = wincap.translate_to_screen_coords(best_match)
            print(f"Best crop match at: {best_abs}")
            pg.moveTo(best_abs[0], best_abs[1])
            pg.rightClick()

            time.sleep(1.5)

            screenshot_after_click = wincap.get_screenshot()
            grab_point = vision_button.find_best_match(screenshot_after_click, threshold=0.97)

            if grab_point is not None:
                grab_abs = wincap.translate_to_screen_coords(grab_point)
                print(f"Grab button found at: {grab_abs}")
                pg.moveTo(grab_abs[0], grab_abs[1])
                pg.click()
                print("🌱 Raccolto!")

                time.sleep(6)

            else:
                print("⚠️ Bottone 'getCrops' non trovato, riprovo.")
                time.sleep(1)
        else:
            print("✅ Nessun seme visibile, spostati o attendi.")
            break




def harvestSeed(seedPath,cropPath):
    focus_window()
    vision_button = Vision('dataset/buttons/grabSeeds.png', cv.TM_CCOEFF_NORMED)
    vision_crops = Vision(seedPath, cv.TM_SQDIFF_NORMED)  # conferma metodo
    while True:
        screenshot = wincap.get_screenshot()
        best_match = vision_crops.find_best_match(screenshot, threshold=0.21)

        if best_match is not None:
            best_abs = wincap.translate_to_screen_coords(best_match)
            print(f"Best crop match at: {best_abs}")
            pg.moveTo(best_abs[0], best_abs[1])
            pg.rightClick()

            time.sleep(1.5)

            screenshot_after_click = wincap.get_screenshot()
            grab_point = vision_button.find_best_match(screenshot_after_click, threshold=0.97)

            if grab_point is not None:
                grab_abs = wincap.translate_to_screen_coords(grab_point)
                print(f"Grab button found at: {grab_abs}")
                pg.moveTo(grab_abs[0], grab_abs[1])
                pg.click()
                print("🌱 Raccolto!")

                time.sleep(6)
                harvestCrop(cropPath)
            else:
                print("⚠️ Bottone 'grabSeeds' non trovato, riprovo.")
                time.sleep(1)
        else:
            print("✅ Nessun seme visibile, spostati o attendi.")
            break

    print('Done.')

def harvestSeedAndCrops(seedPath,cropPath):
    focus_window()
    vision_buttonGrab = Vision('dataset/buttons/grabSeeds.png', cv.TM_CCOEFF_NORMED)
    vision_seed = Vision(seedPath, cv.TM_SQDIFF_NORMED)  # conferma metodo
    vision_buttonHarvest = Vision('dataset/buttons/getCrops.png', cv.TM_CCOEFF_NORMED)
    vision_crops = Vision(cropPath, cv.TM_SQDIFF_NORMED)  # conferma metodo
    while True:
        checkCap()
        screenshot = wincap.get_screenshot()
        best_match = vision_seed.find_best_match(screenshot, threshold=0.21)

        if best_match is not None:
            best_abs = wincap.translate_to_screen_coords(best_match)
            print(f"Best crop match at: {best_abs}")
            pg.moveTo(best_abs[0], best_abs[1])
            pg.rightClick()

            time.sleep(1.5)

            screenshot_after_click = wincap.get_screenshot()
            grab_point = vision_buttonGrab.find_best_match(screenshot_after_click, threshold=0.97)

            if grab_point is not None:
                grab_abs = wincap.translate_to_screen_coords(grab_point)
                print(f"Grab button found at: {grab_abs}")
                pg.moveTo(grab_abs[0], grab_abs[1])
                pg.click()
                print("🌱 Raccolto!")

                time.sleep(6)

                    
            else:
                print("⚠️ Bottone 'grabSeeds' non trovato, riprovo.")
                time.sleep(1)
            
            ###harvest 
            checkCap()
            screenshot = wincap.get_screenshot()
            best_match = vision_crops.find_best_match(screenshot, threshold=0.22)
            if best_match is not None:
                best_abs = wincap.translate_to_screen_coords(best_match)
                print(f"Best crop match at: {best_abs}")
                pg.moveTo(best_abs[0], best_abs[1])
                pg.rightClick()
                time.sleep(1.5)

                screenshot_after_click = wincap.get_screenshot()
                grab_point = vision_buttonHarvest.find_best_match(screenshot_after_click, threshold=0.97)

                if grab_point is not None:
                    grab_abs = wincap.translate_to_screen_coords(grab_point)
                    print(f"Grab button found at: {grab_abs}")
                    pg.moveTo(grab_abs[0], grab_abs[1])
                    pg.click()
                    print("🌱 Raccolto!")
                    time.sleep(6)
                        
        else:
            print("✅ Nessun seme visibile, spostati o attendi.")
            break

    print('Done.')

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
    focus_window()
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



while True:
    harvestSeedAndCrops("dataset/seeds/fernWithSeeds.png","dataset/crops/fernCrops.png")
    time.sleep(100)