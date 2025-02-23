def generar_pseudonumeros(semilla_inicial, multiplicador, cantidad):
    pseudonumeros = []
    semilla = semilla_inicial

    for _ in range(cantidad):
        # Paso 1: Multiplicar semilla por multiplicador
        producto = semilla * multiplicador
        
        # Paso 2: Convertir a cadena y rellenar con ceros a la izquierda
        producto_str = f"{producto:08d}"  # Asegura 8 dígitos
        
        # Paso 3: Extraer los 4 dígitos centrales
        centro = producto_str[2:6]  # Los 4 dígitos del medio
        
        # Paso 4: Guardar el pseudonúmero y actualizar la semilla
        pseudonumeros.append(int(centro))
        semilla = int(centro)
    
    return pseudonumeros

# Parámetros
semilla_inicial = 1234
multiplicador = 5678
cantidad = 500

# Generar los pseudonúmeros
pseudonumeros = generar_pseudonumeros(semilla_inicial, multiplicador, cantidad)
print(pseudonumeros)