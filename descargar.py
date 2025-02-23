import cv2
import torch
import numpy as np

# Cargar el modelo preentrenado de YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Ruta de la imagen
#"C:\Users\yahir\Downloads\practicar c\dataset\cargo truck\gettyimages-507121081-612x612.jpg"
#"C:\Users\yahir\Downloads\practicar c\dataset\cargo truck\s-l1200.jpg"
#"C:\Users\yahir\Downloads\practicar c\dataset\cargo truck\61J4zcFVPJL.jpg"
#"C:\Users\yahir\Downloads\practicar c\dataset\cargo truck\D_982315-MLM80289896529_102024-C.jpg"
#"C:\Users\yahir\Downloads\practicar c\dataset\cargo truck\carroRunRun.jpeg"
#"C:\Users\yahir\Downloads\practicar c\dataset\Contenedor\Imagen_29.jpeg"
image_path = 'C:/Users/yahir/Downloads/practicar c/dataset/Contenedor/Imagen_29.jpeg'

# Realizar inferencia en la imagen
results = model(image_path)

# Obtener las detecciones en formato pandas DataFrame
detections = results.pandas().xyxy[0]

# Filtrar vehículos (car, truck, bus)
vehicles = detections[detections['name'].isin(['car', 'truck', 'bus'])]

# Cargar la imagen original
image = cv2.imread(image_path)

# Procesar cada vehículo detectado
for _, vehicle in vehicles.iterrows():
    # Coordenadas del vehículo
    x_min, y_min, x_max, y_max = map(int, vehicle[['xmin', 'ymin', 'xmax', 'ymax']])
    
    # Dibujar el bounding box del vehículo
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # Verde para vehículos
    
    # Recortar la región del vehículo
    vehicle_region = image[y_min:y_max, x_min:x_max]
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(vehicle_region, cv2.COLOR_BGR2GRAY)
    
    # Suavizar la imagen
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Aplicar detección de bordes (Canny)
    edges = cv2.Canny(blurred, 50, 150)
    
    # Crear una máscara para la parte inferior del vehículo
    mask = np.zeros_like(gray)
    mask[int(0.6 * gray.shape[0]):, :] = 255  # Enfocarse en la parte inferior
    masked_edges = cv2.bitwise_and(edges, edges, mask=mask)
    
    # Detectar círculos usando Hough Transform
    circles = cv2.HoughCircles(masked_edges, cv2.HOUGH_GRADIENT, dp=1, minDist=100,
                               param1=100, param2=50, minRadius=20, maxRadius=80)
    
    # Dibujar las ruedas detectadas
    if circles is not None:
        valid_circles = []
        for circle in circles[0]:
            x, y, r = map(int, circle)
            global_x = x + x_min
            global_y = y + y_min
            
            # Verificar si el círculo está en la parte inferior del vehículo
            if y_min + 0.6 * (y_max - y_min) <= global_y <= y_max:
                valid_circles.append(circle)
                cv2.circle(image, (global_x, global_y), r, (0, 0, 255), 2)  # Rojo para ruedas
                cv2.circle(image, (global_x, global_y), 2, (0, 0, 255), 3)  # Centro de la rueda
        
        print(f"Vehículo: {vehicle['name']}, Ruedas válidas detectadas: {len(valid_circles)}")
    else:
        print(f"Vehículo: {vehicle['name']}, No se detectaron ruedas.")

# Mostrar la imagen con los resultados
cv2.imshow("Detecciones", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Guardar la imagen con los resultados
output_path = 'C:/Users/yahir/Downloads/practicar c/dataset/output_with_detections.jpg'
cv2.imwrite(output_path, image)
print(f"Imagen guardada en: {output_path}")