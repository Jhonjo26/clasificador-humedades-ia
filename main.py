import re
from difflib import get_close_matches

# --- Mapeo limpio de selectores (fix problema 5) ---
MAPA_LUGAR = {
    "techo / azotea / terraza": ["terraza", "azotea", "techo"],
    "baño": ["baño"],
    "cocina": ["cocina"],
    "lavadero": ["lavadero"],
    "sótano / subsuelo": ["sótano", "subsuelo"],
    "planta baja": ["planta baja"],
    "otro": []
}

MAPA_ZONA = {
    "húmeda": "húmeda", "tropical": "tropical", "costera": "costera",
    "fría": "fría", "andina": "andina", "patagónica": "patagónica",
    "seca": "seca", "árida": "árida", "desértica": "desértica"
}

# --- Categorías con ID único (fix problema 6) ---
CATEGORIAS = [
    {
        "id": "CAT001",
        "keywords": ["techo", "lluvia", "gotera", "cubierta",
                    "teja", "canaleta", "terraza", "azotea"],
        "categoria": "Filtración por Cubierta / Techo",
        "solucion": "Impermeabilización y revisión de cubierta.",
        "urgencia": "Alta",
        "prioridad": 2,
        "presupuesto": "$500 - $2000 USD",
        "materiales": ["Membrana asfáltica", "Sellador poliuretano",
                      "Pintura impermeabilizante"]
    },
    {
        "id": "CAT002",
        "keywords": ["cimiento", "zócalo", "piso", "subsuelo",
                    "base", "napa"],
        "categoria": "Humedad por Capilaridad (Cimientos)",
        "solucion": "Inyección de resinas o barrera química.",
        "urgencia": "Alta",
        "prioridad": 2,
        "presupuesto": "$800 - $3000 USD",
        "materiales": ["Resina epoxi", "Cristalizante",
                      "Barrera química inyectable"]
    },
    {
        "id": "CAT003",
        "keywords": ["hongo", "ventanal", "ventana", "condensación",
                    "vapor", "baño", "cocina", "lavadero"],
        "categoria": "Humedad por Condensación",
        "solucion": "Ventilación mejorada o placas térmicas.",
        "urgencia": "Media",
        "prioridad": 3,
        "presupuesto": "$200 - $800 USD",
        "materiales": ["Placa de yeso hidrófugo", "Extractor de aire",
                      "Pintura antihumedad"]
    },
    {
        "id": "CAT004",
        "keywords": ["caño", "tubería", "pérdida", "cañería rota"],
        "categoria": "Humedad por Pérdida en Cañería",
        "solucion": "Inspección y reparación de cañerías.",
        "urgencia": "Urgente",
        "prioridad": 1,
        "presupuesto": "$300 - $1500 USD",
        "materiales": ["Cinta selladora", "Masilla hidráulica",
                      "Caños de reemplazo"]
    },
]

ORDEN_URGENCIA = {"Urgente": 1, "Alta": 2, "Media": 3, "A evaluar": 4}


def buscar_keywords(texto: str, keywords: list) -> list:
    """
    Combina re (precisión) + difflib (tolerancia ortográfica).
    """
    palabras_texto = texto.split()
    encontradas = []

    for kw in keywords:
        # Primero: búsqueda exacta por palabra completa con re
        patron = rf"\b{re.escape(kw)}\b"
        if re.search(patron, texto):
            encontradas.append(kw)
        else:
            # Segundo: tolerancia ortográfica con difflib
            similares = get_close_matches(
                kw, palabras_texto, n=1, cutoff=0.82
            )
            if similares:
                encontradas.append(kw)

    return encontradas


def clasificar_humedad(
    descripcion: str,
    lugar: str = "",
    zona_climatica: str = "",
    cerca_del_mar: bool = False
) -> dict:

    # --- Normalización ---
    descripcion = descripcion.lower().strip()

    # Fix problema 2: zona vacía → valor neutro
    zona = MAPA_ZONA.get(zona_climatica.lower().strip(), "no_especificada")

    # Fix problema 5: mapeo limpio de selector compuesto
    lugar_key = lugar.lower().strip()
    lugares = MAPA_LUGAR.get(lugar_key, [])

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
    elif zona in ["fría", "andina", "patagónica"]:
        alertas_zona.append("⚠️ Zona fría: riesgo por dilatación.")
    elif zona in ["seca", "árida", "desértica"]:
        alertas_zona.append("⚠️ Zona seca: revisar napas y cañerías.")

    # --- Lugar físico ---
    alertas_lugar = []
    if any(p in lugares for p in ["sótano", "subsuelo"]):
        alertas_lugar.append("📍 Alto riesgo: revisar capilaridad.")
    if any(p in lugares for p in ["terraza", "azotea", "techo"]):
        alertas_lugar.append("📍 Superficie expuesta: impermeabilizar.")
    if any(p in lugares for p in ["baño", "cocina", "lavadero"]):
        alertas_lugar.append("📍 Zona húmeda: revisar ventilación.")

    # --- Clasificación principal ---
    coincidencias = []
    for cat in CATEGORIAS:
        palabras_encontradas = buscar_keywords(descripcion, cat["keywords"])
        if palabras_encontradas:
            coincidencias.append({
                "id": cat["id"],
                "categoria": cat["categoria"],
                "solucion": cat["solucion"],
                "urgencia": cat["urgencia"],
                "prioridad": cat["prioridad"],
                "presupuesto": cat["presupuesto"],
                "materiales": cat["materiales"],
                "palabras_clave": palabras_encontradas
            })

    # Ordenar por urgencia (fix problema 1 parcial)
    coincidencias.sort(key=lambda x: ORDEN_URGENCIA.get(x["urgencia"], 99))

    # Siempre devuelve lista (fix problema crítico)
    if not coincidencias:
        coincidencias = [{
            "id": "CAT000",
            "categoria": "Inspección General Necesaria",
            "solucion": "Diagnóstico no concluyente. Visita técnica.",
            "urgencia": "A evaluar",
            "prioridad": 99,
            "presupuesto": "A determinar",
            "materiales": [],
            "palabras_clave": []
        }]

    return {
        "diagnostico": coincidencias,
        "alertas_zona": alertas_zona,
        "alertas_lugar": alertas_lugar,
        "alertas_salinidad": alertas_salinidad
    }


# --- Prueba ---
resultado = clasificar_humedad(
    descripcion="Tengo gotera en el teco y hongos en la cocina",
    lugar="techo / azotea / terraza",
    zona_climatica="húmeda",
    cerca_del_mar=True
)

for key, val in resultado.items():
    print(f"\n{key.upper()}:")
    print(val)
