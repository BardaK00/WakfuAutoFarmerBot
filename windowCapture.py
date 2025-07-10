import numpy as np
import win32gui, win32ui, win32con


class WindowCapture:
    # Dimensioni dell'immagine catturata
    w = 1920
    h = 1080

    # Handle della finestra
    hwnd = None

    # Offset per ritagliare i bordi della finestra
    cropped_x = 0
    cropped_y = 0

    # Offset assoluto della finestra sullo schermo (per il clic)
    offset_x = 0
    offset_y = 0

    def __init__(self, window_name='WAKFU'):
        # Trova la finestra in base al titolo
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            self.list_window_names()
            raise Exception(f'Finestra non trovata: "{window_name}"')

        # Ottieni le dimensioni esterne della finestra
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # Escludi i bordi e la barra del titolo
        border_pixels = 8
        titlebar_pixels = 30
        self.w -= border_pixels * 2
        self.h -= titlebar_pixels + border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # Calcola l'offset assoluto sullo schermo
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):
        """
        Cattura uno screenshot della finestra target.
        Restituisce un'immagine RGB compatibile con OpenCV.
        """
        # Ottieni il device context (DC) della finestra
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()

        # Crea bitmap compatibile e selezionala
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)

        # Copia l'area ritagliata della finestra nel DC compatibile
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # Estrai i dati in formato grezzo
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')  # Corretto rispetto a fromstring (deprecato)
        img.shape = (self.h, self.w, 4)  # BGRA

        # Libera le risorse
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Rimuove il canale alpha per compatibilità con cv.matchTemplate
        img = img[:, :, :3]

        # Assicura che l'immagine sia contigua in memoria
        img = np.ascontiguousarray(img)

        return img

    def get_screen_position(self, pos):
        """
        Converte una coordinata (x, y) relativa allo screenshot
        in coordinate assolute dello schermo.
        """
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

    def list_window_names(self):
        """
        Stampa tutte le finestre visibili per aiutarti a trovare
        il titolo corretto da usare nel costruttore.
        """
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    def translate_to_screen_coords(self, points):
    
        if isinstance(points, tuple) and len(points) == 2 and all(isinstance(c, int) for c in points):
            return (points[0] + self.offset_x, points[1] + self.offset_y)
        else:
            return [(x + self.offset_x, y + self.offset_y) for (x, y) in points]

