import cv2 as cv
import os
import time
from windowCapture import WindowCapture
from vision import Vision
import pyautogui as pg
import math
import pygetwindow as gw
import keyboard
import win32gui
import win32con
import win32com.client


def focus_window():
    try:
        win = gw.getWindowsWithTitle("WAKFU")[0]
        if win.isMinimized:
            win.restore()
            time.sleep(0.2)
        win.activate()
        time.sleep(0.2)

        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')  # trucco ALT
        hwnd = win._hWnd
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwnd)

        print("✅ WAKFU in foreground")
        return True
    except Exception as e:
        print("❌ Errore focus:", e)
        return False


os.chdir(os.path.dirname(os.path.abspath(__file__)))

wincap = WindowCapture()
wincap.list_window_names()



def harvest():
    vision_button = Vision('grabSeeds.png', cv.TM_CCOEFF_NORMED)
    vision_crops = Vision('1.png', cv.TM_SQDIFF_NORMED)  # conferma metodo
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
            else:
                print("⚠️ Bottone 'grabSeeds' non trovato, riprovo.")
                time.sleep(1)
        else:
            print("✅ Nessun seme visibile, spostati o attendi.")
            break

    print('Done.')




def getSeed(cropPath):
    vision_seed = Vision(cropPath,cv.TM_CCOEFF_NORMED)
    ###### enter the game #####
    focus_window()
    #####open inventory######
    print("apro l'invetario")
    time.sleep(2)
    pg.press('i')
    time.sleep(0.5)
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
    select = int(input())
    if select == 1:
        getSeed("dataset/seeds/fernSeed.png")


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
            if count_plant ==25:
                print("massimo piante da piantare raggiunto mi fermo")
                break


plant()