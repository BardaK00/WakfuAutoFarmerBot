import cv2 as cv
import numpy as np
import os
import time
from windowCapture import WindowCapture
from vision import Vision
import pyautogui as pg
import math
import pygetwindow as gw
from focus_window import focusWindow

wincap = WindowCapture()
wincap.list_window_names()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def getCrops():
    vision_buttonHarvest = Vision('dataset/buttons/getCrops.png', cv.TM_CCOEFF_NORMED)
    screenshot = wincap.get_screenshot()
    best_match = vision_buttonHarvest.find_best_match(screenshot, threshold=0.95)
    if best_match is not None:
        pos = wincap.translate_to_screen_coords(best_match)
        pg.moveTo(pos)
        time.sleep(0.5)
        pg.click()
        time.sleep(6)

def harvestSeedAndCrops(seedPath):
    orient = ["dataset/charOrientation/left.png",
          "dataset/charOrientation/right.png",
          "dataset/charOrientation/nord.png",
          "dataset/charOrientation/south.png"] 
    
    focusWindow()
    vision_buttonGrab = Vision('dataset/buttons/grabSeeds.png', cv.TM_CCOEFF_NORMED)
    vision_seed = Vision(seedPath, cv.TM_SQDIFF_NORMED)

    screen_width, screen_height = pg.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    
    while True:
        screenshot = wincap.get_screenshot()
        best_match = vision_seed.find_best_match(screenshot, threshold=0.21)
        if best_match is None:
            print("⏹️ Nessun seme visibile, uscita.")
            break
        
        # SALVA LA POSIZIONE ORIGINALE DEL SEME
        seed_pos_original = wincap.translate_to_screen_coords(best_match)
        print(f"🌱 Seme trovato a: {seed_pos_original}")
        
        # Clicca sul seme
        pg.moveTo(seed_pos_original[0], seed_pos_original[1])
        pg.rightClick()
        print(f"Right click su seme a {seed_pos_original}")
        time.sleep(0.5)  # attesa dopo right click
        
        # Trova e clicca il bottone grabSeeds
        screenshot_after_click = wincap.get_screenshot()
        grab_match = vision_buttonGrab.find_best_match(screenshot_after_click, threshold=0.97)
        if grab_match is None:
            print("⚠️ Bottone 'grabSeeds' non trovato, riprovo.")
            time.sleep(1)
            continue
        
        grab_pos = wincap.translate_to_screen_coords(grab_match)
        print(f"🔘 Bottone 'grabSeeds' trovato a: {grab_pos}")
        pg.moveTo(grab_pos[0], grab_pos[1])
        pg.click()
        print("✅ Semi raccolti!")
        time.sleep(6)  # aspetta raccolta semi
        
        # RICONOSCE L'ORIENTAMENTO DEL PERSONAGGIO
        screenshot_after_gather = wincap.get_screenshot()
        best_orientation = None
        orientation_names = ["left", "right", "nord", "south"]
        
        for i, orient_path in enumerate(orient):
            vision_orient = Vision(orient_path, cv.TM_CCOEFF_NORMED)
            orient_match = vision_orient.find_best_match(screenshot_after_gather, threshold=0.8)
            
            if orient_match is not None:
                print(f"🧭 Orientamento {orientation_names[i]} trovato!")
                best_orientation = i
                break  # Prende il primo orientamento trovato
        
        if best_orientation is not None:
            print(f"🎯 Orientamento rilevato: {orientation_names[best_orientation]}")
            
            # Sposta il mouse in base all'orientamento
            if best_orientation == 0:  # left
                pg.moveTo(center_x-50, center_y+50)
                pg.rightClick()
                time.sleep(0.5)
                getCrops()
                
            elif best_orientation == 1:  # right
                pg.moveTo(center_x+50, center_y-50)
                pg.rightClick()
                time.sleep(0.5)
                getCrops()
                
            elif best_orientation == 2:  # nord
                pg.moveTo(center_x-50, center_y-50)
                pg.rightClick()
                time.sleep(0.5)
                getCrops()
                
            elif best_orientation == 3:  # south
                pg.moveTo(center_x+50, center_y+50)
                pg.rightClick()
                time.sleep(0.5)
                getCrops()
            
           