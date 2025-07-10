import cv2 as cv
from vision import Vision
from windowCapture import WindowCapture
import numpy as np

def draw_point(image, point, color=(0, 255, 0), radius=10):
    """Disegna un cerchio nel punto dato."""
    x, y = int(point[0]), int(point[1])
    cv.circle(image, (x, y), radius, color, 2)
    return image

def main():
    # Cattura finestra attiva
    wincap = WindowCapture()

    # Fai screenshot della finestra
    screenshot = wincap.get_screenshot()

    # Inizializza Vision con metodo CCOEFF_NORMED
    vision_button = Vision("grabSeeds.png", method=cv.TM_CCOEFF_NORMED)

    # Trova il miglior punto
    best_point = vision_button.find_best_match(screenshot, threshold=0.8)

    if best_point is not None:
        print(f"✅ Miglior punto trovato (relativo): {best_point}")

        # Converti in coordinate assolute
        screen_point = wincap.translate_to_screen_coords([best_point])[0]
        print(f"📍 Coordinate assolute (per pyautogui): {screen_point}")

        # Disegna il punto
        debug_img = draw_point(screenshot.copy(), best_point, color=(0, 0, 255))

        # Salva immagine per verifica manuale
        cv.imwrite("debug_grab_match.png", debug_img)
        print("💾 Immagine salvata in 'debug_grab_match.png'")

        # Mostra a schermo
        cv.imshow("DEBUG MATCH", debug_img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        print("❌ Nessun match sopra la soglia trovata.")

if __name__ == "__main__":
    main()
