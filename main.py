 def clasificar_humedad(descripcion: str, lugar: str = "", zona_climatica: str = "") -> dict:
    descripcion = descripcion.lower()
    lugar = lugar.lower()
    zona = zona_climatica.lower()

    categorias = [
        {
            "keywords": ["techo", "lluvia", "gotera", "cubierta", "teja", "canaleta"],
            "categoria": "Filtración por Cubierta / Techo",
            "solucion": "Requiere impermeabilización y revisión de cubierta."
        },
        {
            "keywords": ["cimiento", "zócalo", "abajo", "piso", "subsuelo", "base"],
            "categoria": "Humedad por Capilaridad (Cimientos)",
            "solucion": "Requiere inyección de resinas o barrera química."
        },
        {
            "keywords": ["hongo", "ventanal", "ventana", "condensación", "vapor", "baño", "cocina"],
            "categoria": "Humedad por Condensación",
            "solucion": "Requiere ventilación mejorada o placas térmicas."
        },
        {
            "keywords": ["caño", "tubería", "pérdida", "agua corriente", "filtro lateral"],
            "categoria": "Humedad por Pérdida en Cañería",
            "solucion": "Requiere inspección de cañerías y reparación de pérdidas."
        },
    ]

    # --- Alertas por zona climática ---
    alertas_zona = []
    if zona in ["húmeda", "tropical", "costera"]:
        alertas_zona.append("⚠️ Zona húmeda: mayor riesgo de condensación y hongos.")
    if zona in ["fría", "andina", "patagónica"]:
        alertas_zona.append("⚠️ Zona fría: mayor riesgo de filtraciones por dilatación de materiales.")
    if zona in ["seca", "árida", "desértica"]:
        alertas_zona.append("⚠️ Zona seca: humedad posiblemente por cañerías o napas subterráneas.")

    # --- Alertas por lugar físico ---
    alertas_lugar = []
    if any(p in lugar for p in ["sótano", "subsuelo", "planta baja"]):
        alertas_lugar.append("📍 Lugar de riesgo alto: revisar capilaridad y napas.")
    if any(p in lugar for p in ["terraza", "azotea", "techo"]):
        alertas_lugar.append("📍 Superficie expuesta: priorizar impermeabilización.")
    if any(p in lugar for p in ["baño", "cocina", "lavadero"]):
        alertas_lugar.append("📍 Zona húmeda interior: revisar ventilación y cañerías.")

    # --- Clasificación principal ---
    coincidencias = []
    for cat in categorias:
        palabras_encontradas = [kw for kw in cat["keywords"] if kw in descripcion]
        if palabras_encontradas:
            coincidencias.append({
                "categoria": cat["categoria"],
                "solucion": cat["solucion"],
                "palabras_clave": palabras_encontradas
            })

    if not coincidencias:
        coincidencias = [{
            "categoria": "Inspección General Necesaria",
            "solucion": "Diagnóstico no concluyente. Se recomienda visita técnica.",
            "palabras_clave": []
        }]

    return {
        "diagnostico": coincidencias if len(coincidencias) > 1 else coincidencias[0],
        "alertas_zona": alertas_zona,
        "alertas_lugar": alertas_lugar
    }


# --- Prueba ---
resultado = clasificar_humedad(
    descripcion="Tengo hongos cerca del ventanal de la cocina",
    lugar="cocina, planta baja",
    zona_climatica="húmeda"
)

for key, val in resultado.items():
    print(f"\n{key.upper()}:")
    print(val) 
