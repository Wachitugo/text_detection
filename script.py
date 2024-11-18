import cv2
import numpy as np
import os
import pytesseract

def detect_orientation(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    height = binary.shape[0]

    #dividir la imagen en dos mitades
    top_half = binary[0:int(height/2), :]
    bottom_half = binary[int(height/2):, :]

    #calcular la densidad de pixeles neg
    top_density = np.sum(top_half == 0) / top_half.size
    bottom_density = np.sum(bottom_half == 0) / bottom_half.size

    is_upside_down = (top_density < bottom_density) 

    return {
        'is_upside_down': is_upside_down,
        'rotation_needed': 180 if is_upside_down else 0,
        'top_density': top_density,
        'bottom_density': bottom_density
    }

def rotate_image_if_needed(image):
    # Detectar orientación
    orientation = detect_orientation(image)

    # Rotar si es necesario
    if orientation['is_upside_down']:
        # Obtener dimensiones
        height, width = image.shape[:2]
        # Calcular el centro
        center = (width/2, height/2)
        # Crear matriz de rotación
        rotation_matrix = cv2.getRotationMatrix2D(center, 180, 1.0)
        # Realizar la rotación
        rotated = cv2.warpAffine(image, rotation_matrix, (width, height))
        return rotated

    return image


def detect_number_roi(image):
    # Convertir a escala de grises si es necesario
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    height = gray.shape[0]
    roi = gray[0:int(height/2), :]  # la parte de arriba

    # Redimensionar
    scale_factor = 4
    resized = cv2.resize(roi, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

    # Mejorar el contraste    mm falta ajustar
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8,8))
    contrast = clahe.apply(resized)

    # Binarizar
    _, binary = cv2.threshold(contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    #aplicar operaciones morfológicas para arreglar la imagen
    kernel = np.ones((3,3), np.uint8)
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return morph

def read_number_focused(image):
    processed = detect_number_roi(image)
    
    configs = [
        r'--oem 3 --psm 7',  # Una línea
        r'--oem 3 --psm 8',  # Una palabra
        r'--oem 3 --psm 13',  # Línea sin formato
        r'--oem 3 --psm 6'   # Bloque uniforme
    ]
    for config in configs:
        text = pytesseract.image_to_string(
            processed,
            config=config + ' -c tessedit_char_whitelist=0123456789'
        ).strip()

        if text.isdigit():
            return text

    return text

input_folder = "images"
numeroant = None  
numeros_detectados = []

def son_similares(num1, num2, tolerancia=2):
    diferencias = sum(1 for a, b in zip(num1, num2) if a != b)
    return diferencias <= tolerancia

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        input_path = os.path.join(input_folder, filename)

        image = cv2.imread(input_path)
        rotated_image = rotate_image_if_needed(np.array(image))
        numero = read_number_focused(rotated_image)

        if len(str(numero)) >= 6 and numeroant != numero:
            if not any(son_similares(numero, n) for n in numeros_detectados[:6]):
                print(f'{filename}: {numero}')
                numeros_detectados.append(numero)
                numeroant = numero