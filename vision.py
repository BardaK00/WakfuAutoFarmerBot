import cv2 as cv
import numpy as np

# Carica immagine base e template senza preprocessing
import cv2 as cv
import numpy as np

class Vision:
    def __init__(self, crop_img_path, method=cv.TM_SQDIFF_NORMED):
        self.template = cv.imread(crop_img_path, cv.IMREAD_UNCHANGED)
        if self.template is None:
            raise ValueError(f"Template non trovato: {crop_img_path}")
        self.crop_w, self.crop_h = self.template.shape[1], self.template.shape[0]
        self.method = method

    def find(self, base_img, goodMatch=0.258):
        # Se viene passato un path, carica l'immagine
        if isinstance(base_img, str):
            imgBase = cv.imread(base_img, cv.IMREAD_UNCHANGED)
            if imgBase is None:
                raise ValueError(f"Immagine base non trovata: {base_img}")
        elif isinstance(base_img, np.ndarray):
            imgBase = base_img
        else:
            raise TypeError("Input non valido. Deve essere un percorso immagine o un array NumPy.")

        # Usa solo il primo canale (es. Blue)
        imgBase_ch = imgBase[:, :, 0]
        template_ch = self.template[:, :, 0]

        # Match
        res = cv.matchTemplate(imgBase_ch, template_ch, self.method)
        locations = np.where(res <= goodMatch)
        locations = list(zip(*locations[::-1]))  # (x, y)

        # Crea rettangoli per ogni match trovato
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.crop_w, self.crop_h]
            rectangles.append(rect)

        # Raggruppa rettangoli per evitare duplicati
        rectangles, _ = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        # Calcola centri
        points = []
        for (x, y, w, h) in rectangles:
            center_x = x + w // 2
            center_y = y + h // 2
            points.append((center_x, center_y))

        return points
    

    def find_best_match(self, base_img, threshold=0.85):
        """
        Restituisce il miglior punto (x, y) centro del match se supera la soglia.
        Altrimenti restituisce None.
        """
        if isinstance(base_img, str):
            base_img = cv.imread(base_img, cv.IMREAD_UNCHANGED)
            if base_img is None:
                raise ValueError("Immagine non trovata:", base_img)

        img_ch = base_img[:, :, 0]
        template_ch = self.template[:, :, 0]

        res = cv.matchTemplate(img_ch, template_ch, self.method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        if self.method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            match_value = min_val
            match_loc = min_loc
            if match_value > threshold:
                return None
        else:
            match_value = max_val
            match_loc = max_loc
            if match_value < threshold:
                return None

        # Calcola centro
        center_x = match_loc[0] + self.crop_w // 2
        center_y = match_loc[1] + self.crop_h // 2

        return (center_x, center_y)
