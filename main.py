def clasificar_humedad(descripcion_cliente):
    descripcion = descripcion_cliente.lower()
    
    if "techo" in descripcion or "lluvia" in descripcion:
        return "Categoría: Filtración por Cubierta / Techo. Requiere impermeabilización."
    elif "abajo" in descripcion or "cimiento" in descripcion or "zócalo" in descripcion:
        return "Categoría: Humedad por Capilaridad (Cimientos). Requiere inyección de resinas."
    elif "hongo" in descripcion or "ventanal" in descripcion:
        return "Categoría: Humedad por Condensación. Requiere ventilación o placas térmicas."
    else:
        return "Categoría: Inspección General Necesaria. Diagnóstico no concluyente."

mensaje_cliente = "Tengo manchas negras y hongos cerca del ventanal de la cocina"
resultado = clasificar_humedad(mensaje_cliente)
print(resultado)
