 def clasificar_humedad(descripcion: str, lugar: str = "", 
                        zona_climatica: str = "", 
                        cerca_del_mar: bool = False) -> dict:

    descripcion = descripcion.lower()
    lugar = lugar.lower()
    zona = zona_climatica.lower()

    categorias = [
        {
            "keywords": ["techo", "lluvia", "gotera", "cubierta", "teja", 
                        "canaleta", "terraza", "azotea"],
            "categoria": "Filtración por Cubierta / Techo",
            "solucion": "Impermeabilización y revisión de cubierta.",
            "urgencia": "Alta",
            "presupuesto": "$500 - $2000 USD",
            "materiales": ["Membrana asfáltica", "Sellador poliuretano", 
                          "Pintura impermeabilizante"]
        },
        {
            "keywords": ["cimiento", "zócalo", "abajo", "piso", 
                        "subsuelo", "base", "napa"],
            "categoria": "Humedad por Capilaridad (Cimientos)",
            "solucion": "Inyección de resinas o barrera química.",
            "urgencia": "Alta",
            "presupuesto": "$800 - $3000 USD",
            "materiales": ["Resina epoxi", "Cristalizante", 
                          "Barrera química inyectable"]
        },
        {
            "keywords": ["hongo", "ventanal", "ventana", "condensación", 
                        "vapor", "baño", "cocina", "lavadero"],
            "categoria": "Humedad por Condensación",
            "solucion": "Ventilación mejorada o placas térmicas.",
            "urgencia": "Media",
            "presupuesto": "$200 - $800 USD",
            "materiales": ["Placa de yeso hidrófugo", "Extractor de aire", 
                          "Pintura antihumedad"]
        },
        {
            "keywords": ["caño", "tubería", "pérdida", "agua corriente", 
                        "filtro lateral", "canería rota"],
            "categoria": "Humedad por Pérdida en Cañería",
            "solucion": "Inspección y reparación de cañerías.",
            "urgencia": "Urgente",
            "presupuesto": "$300 - $1500 USD",
            "materiales": ["Cinta selladora", "Masilla hidráulica", 
                          "Caños de reemplazo"]
        },
    ]

    # --- Salinidad ---
    alertas_salinidad = []
    if cerca_del_mar:
        alertas_salinidad = [
            "🌊 Zona costera: la sal marina acelera el deterioro.",
            "⚠️ Usar materiales resistentes a la corrosión salina.",
            "🔧 Revisiones periódicas cada 6 meses recomendadas.",
            "🧱 Priorizar revestimientos antisal en fachadas."
        ]

    # --- Zona climática ---
    alertas_zona = []
    if zona in ["húmeda", "tropical", "costera"]:
        alertas_zona.append("⚠️ Zona húmeda: mayor riesgo de hongos.")
    if zona in ["fría", "andina", "patagónica"]:
        alertas_zona.append("⚠️ Zona fría: riesgo por dilatación de materiales.")
    if zona in ["seca", "árida", "desértica"]:
        alertas_zona.append("⚠️ Zona seca: revisar napas y cañerías.")

    # --- Lugar físico ---
    alertas_lugar = []
    if any(p in lugar for p in ["sótano", "subsuelo", "planta baja"]):
        alertas_lugar.append("📍 Alto riesgo: revisar capilaridad y napas.")
    if any(p in lugar for p in ["terraza", "azotea", "techo"]):
        alertas_lugar.append("📍 Superficie expuesta: impermeabilizar.")
    if any(p in lugar for p in ["baño", "cocina", "lavadero"]):
        alertas_lugar.append("📍 Zona húmeda: revisar ventilación y cañerías.")

    # --- Clasificación + urgencia + presupuesto ---
    coincidencias = []
    for cat in categorias:
        palabras_encontradas = [kw for kw in cat["keywords"] 
                                if kw in descripcion]
        if palabras_encontradas:
            coincidencias.append({
                "categoria": cat["categoria"],
                "solucion": cat["solucion"],
                "urgencia": cat["urgencia"],
                "presupuesto": cat["presupuesto"],
                "materiales": cat["materiales"],
                "palabras_clave": palabras_encontradas
            })

    if not coincidencias:
        coincidencias = [{
            "categoria": "Inspección General Necesaria",
            "solucion": "Diagnóstico no concluyente. Visita técnica recomendada.",
            "urgencia": "A evaluar",
            "presupuesto": "A determinar",
            "materiales": [],
            "palabras_clave": []
        }]

    return {
        "diagnostico": coincidencias if len(coincidencias) > 1 else coincidencias[0],
        "alertas_zona": alertas_zona,
        "alertas_lugar": alertas_lugar,
        "alertas_salinidad": alertas_salinidad
    }


# --- Prueba ---
resultado = clasificar_humedad(
    descripcion="Tengo gotera en el techo y hongos en la cocina",
    lugar="terraza, cocina",
    zona_climatica="húmeda",
    cerca_del_mar=True
)

for key, val in resultado.items():
    print(f"\n{key.upper()}:")
    print(val)
