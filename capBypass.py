import cv2
import numpy as np
import os
from pathlib import Path

def debug_template_matching():
    """Funzione di debug per capire cosa non funziona"""
    
    img_path = "cap/base1.png"
    dataset_folder = "cap/face"
    
    print("=== DEBUG TEMPLATE MATCHING ===")
    print(f"Immagine target: {img_path}")
    print(f"Dataset folder: {dataset_folder}")
    print()
    
    # 1. Verifica esistenza file
    print("1. VERIFICA FILE:")
    img_exists = Path(img_path).exists()
    dataset_exists = Path(dataset_folder).exists()
    
    print(f"   Immagine esiste: {img_exists}")
    print(f"   Dataset esiste: {dataset_exists}")
    
    if not img_exists:
        print("   ❌ ERRORE: Immagine non trovata!")
        return
    
    if not dataset_exists:
        print("   ❌ ERRORE: Cartella dataset non trovata!")
        return
    
    # 2. Carica immagine target
    print("\n2. CARICAMENTO IMMAGINE TARGET:")
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print("   ❌ ERRORE: Impossibile caricare l'immagine!")
        return
    
    print(f"   Dimensioni immagine: {img.shape}")
    print(f"   Tipo: {img.dtype}")
    print(f"   Min/Max valori: {img.min()}/{img.max()}")
    
    # 3. Verifica template nel dataset
    print("\n3. VERIFICA TEMPLATE NEL DATASET:")
    template_files = []
    
    for file in os.listdir(dataset_folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            template_files.append(file)
    
    print(f"   Template trovati: {len(template_files)}")
    
    if len(template_files) == 0:
        print("   ❌ ERRORE: Nessun template trovato!")
        return
    
    for file in template_files:
        print(f"   - {file}")
    
    # 4. Test di matching su ogni template
    print("\n4. TEST MATCHING SU OGNI TEMPLATE:")
    
    file_da_escludere = ["escl1.png", "escl2.png", "escl3.png"]
    soglie_test = [0.5, 0.6, 0.7, 0.8, 0.9]
    
    matches_trovati = []
    
    for template_file in template_files:
        # Controllo esclusione migliorato - confronto case-insensitive
        escluso = False
        for file_esclusione in file_da_escludere:
            if template_file.lower() == file_esclusione.lower():
                escluso = True
                break
        
        if escluso:
            print(f"   ⏩ {template_file} - ESCLUSO (trovato in lista esclusione)")
            continue
        
        template_path = os.path.join(dataset_folder, template_file)
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        
        if template is None:
            print(f"   ❌ {template_file} - IMPOSSIBILE CARICARE")
            continue
        
        h, w = template.shape
        area = w * h
        
        print(f"   🔍 {template_file}:")
        print(f"      Dimensioni: {w}x{h} (area: {area})")
        
        # Verifica se template è più grande dell'immagine
        if h > img.shape[0] or w > img.shape[1]:
            print(f"      ❌ Template troppo grande per l'immagine!")
            continue
        
        # Test matching con diverse soglie
        try:
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            max_val = np.max(res)
            min_val = np.min(res)
            
            print(f"      Matching result - Min: {min_val:.3f}, Max: {max_val:.3f}")
            
            # Conta matches per ogni soglia
            for soglia in soglie_test:
                locations = np.where(res >= soglia)
                count = len(locations[0])
                
                if count > 0:
                    print(f"      Soglia {soglia}: {count} matches")
                    matches_trovati.append({
                        'template': template_file,
                        'soglia': soglia,
                        'count': count,
                        'max_val': max_val
                    })
        
        except Exception as e:
            print(f"      ❌ ERRORE nel matching: {e}")
    
    # 5. Riepilogo risultati
    print("\n5. RIEPILOGO RISULTATI:")
    
    if not matches_trovati:
        print("   ❌ NESSUN MATCH TROVATO con nessuna soglia!")
        print("   Possibili cause:")
        print("   - Template troppo diversi dall'immagine target")
        print("   - Immagine target corrotta o molto diversa")
        print("   - Tutti i template sono nella lista di esclusione")
        
        # Mostra il miglior match per template
        print("\n   MIGLIOR MATCH PER TEMPLATE:")
        for template_file in template_files:
            if template_file.lower() in [f.lower() for f in file_da_escludere]:
                continue
            
            template_path = os.path.join(dataset_folder, template_file)
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            
            if template is None:
                continue
            
            if template.shape[0] > img.shape[0] or template.shape[1] > img.shape[1]:
                continue
            
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            max_val = np.max(res)
            max_loc = np.unravel_index(np.argmax(res), res.shape)
            
            print(f"   {template_file}: max correlation = {max_val:.3f}")
    
    else:
        print(f"   ✅ TROVATI {len(matches_trovati)} matches!")
        
        # Mostra i migliori matches
        matches_trovati.sort(key=lambda x: x['max_val'], reverse=True)
        
        print("   TOP 5 MATCHES:")
        for i, match in enumerate(matches_trovati[:5]):
            print(f"   {i+1}. {match['template']}: {match['count']} matches con soglia {match['soglia']} (max: {match['max_val']:.3f})")

def test_matching_semplice():
    """Test di matching molto semplice, equivalente al codice originale"""
    
    print("\n=== TEST MATCHING SEMPLICE (COME ORIGINALE) ===")
    
    img_path = "cap/base1.png"
    dataset_folder = "cap/face"
    threshold = 0.7
    file_da_escludere = []  # Nessun file da escludere per ora
    
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("❌ Impossibile caricare l'immagine")
        return
    
    rettangoli = []
    
    for nome_file in sorted(os.listdir(dataset_folder)):
        # Controllo esclusione migliorato
        escluso = False
        for file_esclusione in file_da_escludere:
            if nome_file.lower() == file_esclusione.lower():
                escluso = True
                break
        
        if escluso:
            print(f"⏩ File escluso: {nome_file}")
            continue
        
        template_path = os.path.join(dataset_folder, nome_file)
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        
        if template is None:
            print(f"⚠️ Template non leggibile: {nome_file}")
            continue
        
        print(f"🔍 Processando: {nome_file}")
        
        try:
            res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            h, w = template.shape
            
            loc = np.where(res >= threshold)
            matches = len(loc[0])
            
            print(f"   Matches trovati: {matches}")
            
            for pt in zip(*loc[::-1]):
                rettangoli.append([pt[0], pt[1], w, h])
                
        except Exception as e:
            print(f"   ❌ Errore: {e}")
    
    print(f"\nTotale rettangoli prima del grouping: {len(rettangoli)}")
    
    if len(rettangoli) > 0:
        # Applica groupRectangles come nel codice originale
        try:
            rettangoli_numpy = np.array(rettangoli)
            gruppi, _ = cv2.groupRectangles(rettangoli_numpy.tolist(), groupThreshold=1, eps=0.5)
            print(f"Gruppi finali: {len(gruppi)}")
            
            # Visualizza risultati
            if len(gruppi) > 0:
                img_color = cv2.imread(img_path)
                for (x, y, w, h) in gruppi:
                    cv2.rectangle(img_color, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                cv2.imshow("Risultati", img_color)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        
        except Exception as e:
            print(f"❌ Errore nel grouping: {e}")
    
    else:
        print("❌ Nessun rettangolo trovato")

def debug_esclusione():
    """Debug specifico per l'esclusione dei file"""
    
    print("=== DEBUG ESCLUSIONE FILE ===")
    
    dataset_folder = "cap/face"
    file_da_escludere = []  # Nessun file da escludere per ora
    
    print(f"Dataset folder: {dataset_folder}")
    print(f"File da escludere: {file_da_escludere}")
    print()
    
    if not Path(dataset_folder).exists():
        print("❌ Cartella dataset non trovata!")
        return
    
    # Lista tutti i file nel dataset
    tutti_i_file = []
    for file in os.listdir(dataset_folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            tutti_i_file.append(file)
    
    print(f"Tutti i file nel dataset ({len(tutti_i_file)}):")
    for file in tutti_i_file:
        print(f"  - {file}")
    
    print()
    
    # Verifica esclusione
    print("Verifica esclusione:")
    file_processati = []
    file_esclusi = []
    
    for file in tutti_i_file:
        escluso = False
        for file_esclusione in file_da_escludere:
            if file.lower() == file_esclusione.lower():
                escluso = True
                file_esclusi.append(file)
                break
        
        if not escluso:
            file_processati.append(file)
    
    print(f"File che verranno processati ({len(file_processati)}):")
    for file in file_processati:
        print(f"  ✅ {file}")
    
    print(f"File esclusi ({len(file_esclusi)}):")
    for file in file_esclusi:
        print(f"  ⏩ {file}")
    
    if len(file_processati) == 0:
        print("❌ ATTENZIONE: Nessun file verrà processato!")
        print("Possibili cause:")
        print("- Tutti i file sono nella lista di esclusione")
        print("- Nessun file immagine nella cartella")
        print("- Problema con i nomi dei file")

def test_face_matching():
    """Test specifico per face matching con parametri ottimizzati"""
    
    print("\n=== TEST FACE MATCHING ===")
    
    img_path = "cap/base1.png"
    dataset_folder = "cap/face"
    
    # Parametri ottimizzati per faces
    soglie_test = [0.4, 0.5, 0.6, 0.7, 0.8]  # Soglie più basse per faces
    
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("❌ Impossibile caricare l'immagine")
        return
    
    print(f"Immagine caricata: {img.shape}")
    
    # Prova anche diversi metodi di matching
    metodi = [
        (cv2.TM_CCOEFF_NORMED, "TM_CCOEFF_NORMED"),
        (cv2.TM_CCORR_NORMED, "TM_CCORR_NORMED"),
        (cv2.TM_SQDIFF_NORMED, "TM_SQDIFF_NORMED")
    ]
    
    best_matches = []
    
    for nome_file in sorted(os.listdir(dataset_folder)):
        if not nome_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
            
        template_path = os.path.join(dataset_folder, nome_file)
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        
        if template is None:
            continue
        
        h, w = template.shape
        area = w * h
        
        print(f"\n🔍 Testing {nome_file} (dimensioni: {w}x{h}, area: {area})")
        
        if h > img.shape[0] or w > img.shape[1]:
            print("   ❌ Template troppo grande")
            continue
        
        # Testa diversi metodi
        for metodo, nome_metodo in metodi:
            try:
                res = cv2.matchTemplate(img, template, metodo)
                
                if metodo == cv2.TM_SQDIFF_NORMED:
                    # Per SQDIFF, valori più bassi sono migliori
                    best_val = np.min(res)
                    print(f"   {nome_metodo}: min = {best_val:.3f}")
                    
                    # Conta matches sotto soglia per SQDIFF
                    for soglia in [0.6, 0.5, 0.4, 0.3]:
                        count = np.sum(res <= soglia)
                        if count > 0:
                            print(f"     Soglia <= {soglia}: {count} matches")
                            best_matches.append({
                                'template': nome_file,
                                'metodo': nome_metodo,
                                'soglia': soglia,
                                'count': count,
                                'best_val': best_val
                            })
                else:
                    # Per altri metodi, valori più alti sono migliori
                    best_val = np.max(res)
                    print(f"   {nome_metodo}: max = {best_val:.3f}")
                    
                    # Conta matches sopra soglia
                    for soglia in soglie_test:
                        count = np.sum(res >= soglia)
                        if count > 0:
                            print(f"     Soglia >= {soglia}: {count} matches")
                            best_matches.append({
                                'template': nome_file,
                                'metodo': nome_metodo,
                                'soglia': soglia,
                                'count': count,
                                'best_val': best_val
                            })
            
            except Exception as e:
                print(f"   ❌ Errore con {nome_metodo}: {e}")
    
    # Mostra i migliori risultati
    if best_matches:
        print(f"\n✅ TROVATI {len(best_matches)} potenziali matches!")
        
        # Ordina per numero di matches
        best_matches.sort(key=lambda x: x['count'], reverse=True)
        
        print("\nTOP 10 MATCHES:")
        for i, match in enumerate(best_matches[:10]):
            print(f"{i+1}. {match['template']} con {match['metodo']}")
            print(f"   Soglia: {match['soglia']}, Matches: {match['count']}, Best: {match['best_val']:.3f}")
    else:
        print("\n❌ Nessun match trovato con nessun metodo")

if __name__ == "__main__":
    debug_esclusione()
    debug_template_matching()
    test_matching_semplice()
    test_face_matching()