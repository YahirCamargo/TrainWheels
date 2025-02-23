from google_images_search import GoogleImagesSearch

# Claves de API de Google Custom Search
API_KEY = "TU_API_KEY"
CX = "TU_CX"

# Inicializar GoogleImagesSearch
gis = GoogleImagesSearch(API_KEY, CX)

# Lista de palabras clave para buscar imágenes
keywords = ["hot wheels sin caja"]

# Número máximo de imágenes por palabra clave
limit = 1000  # Ajusta según necesidad

# Carpeta donde se guardarán las imágenes
output_dir = "dataset"

# Descargar imágenes para cada palabra clave
for keyword in keywords:
    print(f"Descargando imágenes para: {keyword}")
    search_params = {
        'q': keyword,
        'num': limit,
        'safe': 'off',
        'fileType': 'jpg|png',
    }
    
    gis.search(search_params)
    for i, image in enumerate(gis.results(), start=1):
        image.download(output_dir)
        print(f"Imagen {i}/{limit} descargada para: {keyword}")
    
    print(f"Finalizado: {keyword}")

print("Todas las imágenes han sido descargadas.")
