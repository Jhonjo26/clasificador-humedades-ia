import re
from difflib import get_close_matches

MAPA_LUGAR = {
    "techo / azotea / terraza": ["terraza", "azotea", "techo"],
    "baño": ["baño"],
    "cocina": ["cocina"],
    "lavadero": ["lavadero"],
    "sotano / subsuelo": ["sotano", "subsuelo"],
    "planta baja": ["planta baja","pasillo","habitación"],
    "medianera": ["medianera"],
    "exterior / terreno": ["jardin", "pileta", "drenaje", "terreno"],
    "otro": []
}

MAPA_ZONA = {
    "humeda": "humeda", "tropical": "tropical", "costera": "costera",
    "fria": "fria", "andina": "andina", "patagonica": "patagonica",
    "seca": "seca", "arida": "arida", "desertica": "desertica"
}

CATEGORIAS = [
    {
        "id": "CAT001",
        "keywords": ["techo", "lluvia", "chapas", "gotera", "cielorazo","cubierta",
                    "teja", "cargas", "eflorecencia", "manchas oscuras", "canaleta", "terraza", "arriba", "azotea"],
        "categoria": "Filtracion por Cubierta / Techo",
        "solucion": "Impermeabilizacion y revision de cubierta.",
        "urgencia": "Alta",
        "prioridad": 2,
        "presupuesto": "$500 - $2000 USD",
        "materiales": ["Membrana asfaltica", "Sellador poliuretano",
                      "Pintura impermeabilizante"]
    },
    {
        "id": "CAT002",
        "keywords": ["cimiento", "loza", "eflorerescencia", "ceramica", "debajo", "zocalo", "piso", "subsuelo",
                    "base"],
        "categoria": "Humedad por Capilaridad (Cimientos)",
        "solucion": "Inyeccion de resinas o Barrera quimica o Morteros hidrofugos",
        "urgencia": "Alta",
        "prioridad": 2,
        "presupuesto": "$800 - $3000 USD",
        "materiales": ["Resina epoxi", "cemento", "pasta hidrofuga", "Cristalizante",
                      "Barrera quimica inyectable"]
    },
    {
        "id": "CAT003",
        "keywords": ["hongo", "columna", "ventanal", "moho", "pared interior", "condensacion",
                    "vapor", "bano", "cocina", "lavadero"],
        "categoria": "Humedad por Condensacion",
        "solucion": "Ventilacion mejorada o placas termicas y picar raspar pared mas acido muriatico rebajado.",
        "urgencia": "Media",
        "prioridad": 3,
        "presupuesto": "$200 - $800 USD",
        "materiales": ["Placa de yeso hidrofugo", "deshumidificador", "Extractor de aire",
                      "Pintura antihumedad", "acidos curativos de patologias"]
    },
    {
        "id": "CAT004",
        "keywords": ["cano", "tuberia", "perdida", "mancha con bordes", "crece sin lluvia", "caneria rota"],
        "categoria": "Humedad por Perdida en Caneria",
        "solucion": "Inspeccion y reparacion de canerias.",
        "urgencia": "Urgente",
        "prioridad": 1,
        "presupuesto": "$300 - $1500 USD",
        "materiales": ["Cinta selladora", "Masilla hidraulica",
                      "Canos de reemplazo"]
    },
    {
        "id": "CAT005",
        "keywords": ["jardin", "pileta", "drenaje", "terreno",
                    "infiltracion", "exterior"],
        "categoria": "Humedad por Infiltracion Exterior / Terreno",
        "solucion": "Revision de drenajes y sellado perimetral.",
        "urgencia": "Media",
        "prioridad": 3,
        "presupuesto": "$400 - $1800 USD",
        "materiales": ["Geomembrana", "Drenaje frances",
                      "Sellador perimetral"]
    },
    {
        "id": "CAT006",
        "keywords": ["medianera", "vecino", "pared compartida",
                    "lindero", "muro medianero"],
        "categoria": "Humedad por Medianera",
        "solucion": "Coordinacion con vecino y tratamiento de muro.",
        "urgencia": "Media",
        "prioridad": 3,
        "presupuesto": "$300 - $1200 USD",
        "materiales": ["Hidrofugante", "Mortero impermeable",
                      "Membrana liquida"]
    },
    {
        "id": "CAT007",
        "keywords": ["cloaca", "cloacal", "brote", "piso de tierra", "reflujo", "desague",
                    "olor", "pozo"],
        "categoria": "Humedad por Reflujo Cloacal",
        "solucion": "Inspeccion de red cloacal y valvula antirretorno.",
        "urgencia": "Urgente",
        "prioridad": 1,
        "presupuesto": "$500 - $2500 USD",
        "materiales": ["Valvula antirretorno", "Camara de inspeccion",
                      "Sellador cloacal"]
    },
    {
        "id": "CAT008",
        "keywords": ["obra", "construccion", "nuevo", "reciente",
                    "fraguado", "cemento fresco"],
        "categoria": "Humedad por Obra Nueva",
        "solucion": "Tiempo de secado y ventilacion controlada.",
        "urgencia": "Baja",
        "prioridad": 4,
        "presupuesto": "$100 - $500 USD",
        "materiales": ["Deshumidificador", "Ventilacion cruzada",
                      "Pintura transpirable"]
    },{
        "id": "CAT009",
        "keywords": ["napa", "napa freatica", "tierra", "brota del piso",
                    "piso de tierra", "agua subterranea"],
        "categoria": "Humedad por Napa Freatica Alta",
        "solucion": "Drenaje perimetral profundo y bomba sumergible.",
        "urgencia": "Alta",
        "prioridad": 2,
        "presupuesto": "$1000 - $4000 USD",
        "materiales": ["Bomba sumergible", "Drenaje frances",
                      "Geotextil"]
    },    
]

ORDEN_URGENCIA = {
    "Urgente": 1, "Alta": 2, "Media": 3, "Baja": 4, "A evaluar": 5
}


def buscar_keywords(texto, keywords):
    palabras_texto = texto.split()
    encontradas = []
    for kw in keywords:
        patron = rf"\b{re.escape(kw)}\b"
        if re.search(patron, texto):
            encontradas.append(kw)
        else:
            similares = get_close_matches(kw, palabras_texto, n=1, cutoff=0.82)
            if similares:
                encontradas.append(kw)
    return encontradas


def clasificar_humedad(descripcion, lugar="", zona_climatica="", cerca_del_mar=False):
    descripcion = descripcion.lower().strip()
    zona = MAPA_ZONA.get(zona_climatica.lower().strip(), "no_especificada")
    lugares = MAPA_LUGAR.get(lugar.lower().strip(), [])

    alertas_salinidad = []
    if cerca_del_mar:
        alertas_salinidad = [
            "Zona costera: la sal marina acelera el deterioro.",
            "Usar materiales resistentes a la corrosion salina.",
            "Revisiones periodicas cada 6 meses recomendadas.",
            "Priorizar revestimientos antisal en fachadas."
        ]

    alertas_zona = []
    if zona in ["humeda", "tropical", "costera"]:
        alertas_zona.append("Zona humeda: mayor riesgo de hongos.")
    elif zona in ["fria", "andina", "patagonica"]:
        alertas_zona.append("Zona fria: riesgo por dilatacion y congelamiento.")
    elif zona in ["seca", "arida", "desertica"]:
        alertas_zona.append("Zona seca: revisar napas y canerias.")

    alertas_lugar = []
    if any(p in lugares for p in ["sotano", "subsuelo"]):
        alertas_lugar.append("Alto riesgo: revisar capilaridad.")
    if any(p in lugares for p in ["terraza", "azotea", "techo"]):
        alertas_lugar.append("Superficie expuesta: impermeabilizar.")
    if any(p in lugares for p in ["bano", "cocina", "lavadero"]):
        alertas_lugar.append("Zona humeda: revisar ventilacion.")
    if "medianera" in lugares:
        alertas_lugar.append("Medianera: coordinar con vecino lindero.")
    if any(p in lugares for p in ["jardin", "pileta", "drenaje", "terreno"]):
        alertas_lugar.append("Exterior: revisar drenajes perimetrales.")

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

    coincidencias.sort(key=lambda x: ORDEN_URGENCIA.get(x["urgencia"], 99))

    if not coincidencias:
        coincidencias = [{
            "id": "CAT000",
            "categoria": "Inspeccion General Necesaria",
            "solucion": "Diagnostico no concluyente. Visita tecnica.",
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
