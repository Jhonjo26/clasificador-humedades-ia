import streamlit as st
from main import clasificar_humedad
import datetime

st.set_page_config(
    page_title="CasaSana.a.i",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
  :root {
    --naranja: #E86C1A;
    --naranja-claro: #E8A87C;
    --oscuro: #1A1A2E;
    --oscuro-mid: #16213E;
    --oscuro-card: #0F3460;
    --texto: #F0EBE3;
    --texto-suave: #C9B99A;
    --urgente: #FF4C4C;
    --alta: #E86C1A;
    --media: #F5C518;
    --baja: #4CAF50;
    --radio: 12px;
  }
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--oscuro) !important;
    color: var(--texto) !important;
  }
  .stApp {
    background: linear-gradient(160deg, #1A1A2E 0%, #0F3460 60%, #16213E 100%) !important;
    min-height: 100vh;
  }
  .hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    border-bottom: 1px solid rgba(232,108,26,0.25);
    margin-bottom: 2rem;
  }
  .hero-logo {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--naranja);
    letter-spacing: -0.5px;
    line-height: 1;
    margin-bottom: 0.3rem;
    white-space: nowrap;
  }
  .hero-logo span { color: var(--naranja-claro); font-weight: 400; font-size: 1rem; }
  .hero-eslogan {
    font-size: 0.85rem;
    font-weight: 300;
    color: var(--texto-suave);
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .bienvenida-card {
    background: linear-gradient(135deg, rgba(232,108,26,0.15), rgba(232,168,124,0.08));
    border: 1px solid rgba(232,108,26,0.35);
    border-radius: var(--radio);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.8rem;
  }
  .bienvenida-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--naranja);
    margin-bottom: 0.4rem;
  }
  .bienvenida-texto { font-size: 0.88rem; color: var(--texto-suave); line-height: 1.6; margin-bottom: 0.8rem; }
  .bienvenida-beneficio {
    display: inline-block;
    background: rgba(232,108,26,0.2);
    border: 1px solid rgba(232,108,26,0.4);
    border-radius: 20px;
    padding: 0.25rem 0.8rem;
    font-size: 0.78rem;
    color: var(--naranja-claro);
    margin: 0.2rem 0.2rem 0 0;
  }
  .seccion-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--naranja);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 1.4rem;
    margin-bottom: 0.4rem;
  }
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea {
    background-color: rgba(15,52,96,0.6) !important;
    border: 1px solid rgba(232,108,26,0.3) !important;
    border-radius: var(--radio) !important;
    color: var(--texto) !important;
  }
  .stSelectbox > div > div {
    background-color: rgba(15,52,96,0.6) !important;
    border: 1px solid rgba(232,108,26,0.3) !important;
    border-radius: var(--radio) !important;
    color: var(--texto) !important;
  }
  .stSelectbox > div > div > div {
    background-color: #0F3460 !important;
    color: #F0EBE3 !important;
  }
  [data-baseweb="select"] * {
    background-color: #0F3460 !important;
    color: #F0EBE3 !important;
  }
  [data-baseweb="popover"] {
    background-color: #0F3460 !important;
  }
  [data-baseweb="menu"] {
    background-color: #0F3460 !important;
  }
  [data-baseweb="option"] {
    background-color: #0F3460 !important;
    color: #F0EBE3 !important;
  }
  [data-baseweb="option"]:hover {
    background-color: rgba(232,108,26,0.3) !important;
  }
  li[role="option"] {
    background-color: #0F3460 !important;
    color: #F0EBE3 !important;
  }
  .stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label {
    color: #F0EBE3 !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
  }
  .stButton > button {
    background: linear-gradient(135deg, var(--naranja), #C4571A) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radio) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    width: 100% !important;
    padding: 0.7rem 1.5rem !important;
    box-shadow: 0 4px 15px rgba(232,108,26,0.35) !important;
  }
  .resultado-card {
    border-radius: var(--radio);
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
    border-left: 4px solid;
  }
  .resultado-urgente { background: rgba(255,76,76,0.1); border-color: var(--urgente); }
  .resultado-alta { background: rgba(232,108,26,0.12); border-color: var(--alta); }
  .resultado-media { background: rgba(245,197,24,0.1); border-color: var(--media); }
  .resultado-baja { background: rgba(76,175,80,0.1); border-color: var(--baja); }
  .resultado-evaluar { background: rgba(150,150,150,0.1); border-color: #888; }
  .resultado-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--texto);
    margin-bottom: 0.4rem;
  }
  .resultado-presupuesto {
    display: inline-block;
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--naranja-claro);
    background: rgba(232,108,26,0.15);
    border-radius: 8px;
    padding: 0.3rem 0.8rem;
    margin-top: 0.6rem;
  }
  .badge-urgencia {
    display: inline-block;
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.6rem;
  }
  .badge-urgente { background: rgba(255,76,76,0.25); color: #FF8080; }
  .badge-alta { background: rgba(232,108,26,0.25); color: var(--naranja-claro); }
  .badge-media { background: rgba(245,197,24,0.2); color: #F5E06A; }
  .badge-baja { background: rgba(76,175,80,0.2); color: #80C883; }
  .badge-evaluar { background: rgba(150,150,150,0.2); color: #AAAAAA; }
  .alerta-item {
    background: rgba(232,108,26,0.1);
    border: 1px solid rgba(232,108,26,0.3);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin-bottom: 0.4rem;
    font-size: 0.85rem;
    color: var(--naranja-claro);
  }
  .historial-item {
    background: rgba(15,52,96,0.4);
    border: 1px solid rgba(232,108,26,0.15);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.82rem;
  }
  .footer {
    text-align: center;
    padding: 2rem 1rem 1rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(232,108,26,0.15);
    font-size: 0.75rem;
    color: var(--texto-suave);
  }
  .footer strong { color: var(--naranja); }
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
  header { visibility: hidden; }
  /* Visibilidad global */
  p, li, span, div { color: var(--texto); }
  .stMarkdown p { color: #F0EBE3 !important; }
  .stMarkdown li { color: #F0EBE3 !important; }
  .stMarkdown strong { color: #F0EBE3 !important; }
  .stAlert { background: rgba(15,52,96,0.6) !important; color: #F0EBE3 !important; }
  .stRadio > div > label { color: #F0EBE3 !important; font-size:0.95rem !important; }
  [data-testid="stMarkdownContainer"] p { color: #F0EBE3 !important; }
  [data-testid="stMarkdownContainer"] li { color: #F0EBE3 !important; }
</style>
""", unsafe_allow_html=True)

if "historial" not in st.session_state:
    st.session_state.historial = []
if "diagnosticos_total" not in st.session_state:
    st.session_state.diagnosticos_total = 0
if "primer_uso" not in st.session_state:
    st.session_state.primer_uso = True

COLORES = {
    "Urgente": "urgente",
    "Alta": "alta",
    "Media": "media",
    "Baja": "baja",
    "A evaluar": "evaluar",
}


def color_clase(urgencia):
    return COLORES.get(urgencia, "evaluar")


def generar_informe(cliente, resultado, observaciones):
    lineas = [
        "=" * 48,
        "         INFORME CASASANA.A.I",
        "  Inteligencia que cuida. Precision que resuelve.",
        "=" * 48,
        f"Cliente   : {cliente.get('nombre', '')}",
        f"Direccion : {cliente.get('direccion', '')}",
        f"Telefono  : {cliente.get('telefono', '')}",
        f"Fecha     : {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "=" * 48,
        "\nDIAGNOSTICO:",
    ]
    diagnostico = resultado.get("diagnostico", [])
    if isinstance(diagnostico, dict):
        diagnostico = [diagnostico]
    for item in diagnostico:
        lineas += [
            f"\n- {item.get('categoria', '')}",
            f"  Urgencia  : {item.get('urgencia', '')}",
            f"  Solucion  : {item.get('solucion', '')}",
            f"  Presupuesto: {item.get('presupuesto', '')}",
        ]
        if item.get("materiales"):
            lineas.append(f"  Materiales: {', '.join(item['materiales'])}")
    alertas = (
        resultado.get("alertas_zona", []) +
        resultado.get("alertas_lugar", []) +
        resultado.get("alertas_salinidad", [])
    )
    if alertas:
        lineas += ["\nALERTAS:"]
        for a in alertas:
            lineas.append(f"  {a}")
    if observaciones:
        lineas += ["\n" + "-" * 48, "OBSERVACIONES:", observaciones]
    lineas += ["", "=" * 48, "CasaSana.a.i"]
    return "\n".join(lineas)


st.markdown("""
<div class="hero">
  <div class="hero-logo">CasaSana<span>.a.i</span></div>
  <div class="hero-eslogan">Inteligencia que cuida · Precision que resuelve</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.primer_uso:
    st.markdown("""
<div class="bienvenida-card">
  <div class="bienvenida-titulo">Bienvenido a CasaSana.a.i</div>
  <div class="bienvenida-texto">
    sistema de soluciones que analiza,diagnostica y erradica la humedad de casas,comercios y edificios.
  </div>
  <span class="bienvenida-beneficio">Diagnostico instantaneo</span>
  <span class="bienvenida-beneficio">Presupuesto estimado</span>
  <span class="bienvenida-beneficio">Informe descargable</span>
</div>
""", unsafe_allow_html=True)

if st.session_state.diagnosticos_total > 0:
    st.info(f"Diagnosticos en esta sesion: {st.session_state.diagnosticos_total}")

st.markdown('<div class="seccion-label">Datos del cliente</div>', unsafe_allow_html=True)
col1, col2 = st.columns([3, 2])
with col1:
    nombre = st.text_input("Nombre completo", placeholder="Ej: Maria Gonzalez")
with col2:
    telefono = st.text_input("Telefono", placeholder="Ej: 11-4567-8900")
direccion = st.text_input("Direccion del inmueble", placeholder="Ej: Av. Corrientes 1234, CABA")

st.markdown('<div class="seccion-label">Descripcion del problema</div>', unsafe_allow_html=True)
descripcion = st.text_area(
    "Describi el problema con tus palabras e imágenes",
    placeholder="Ej: Hay manchas de humedad en el techo del bano y el piso se esta levantando...",
    height=110,
)
fotos = []
if descripcion.strip():
        st.markdown('<div class="seccion-label">Foto del problema (opcional)</div>', unsafe_allow_html=True)
        if "fotos_guardadas" not in st.session_state:
            st.session_state.fotos_guardadas = []
        fotos_nuevas = st.file_uploader("Subi fotos del problema", type=["jpg","jpeg","png"], accept_multiple_files=True)
        if fotos_nuevas:
            st.session_state.fotos_guardadas = fotos_nuevas 
        fotos = st.session_state.fotos_guardadas
        if fotos:
            st.success(f"✅ {len(fotos)} foto(s) recibida(s).")
st.markdown('<div class="seccion-label">Contexto del inmueble</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    lugar = st.selectbox("Lugar fisico afectado", [
        "no especificado", "techo / azotea / terraza", "baño", "cocina",
        "lavadero", "sotano / subsuelo", "planta baja", "medianera",
        "exterior / terreno", "otro"
    ])
with col4:
    zona_climatica = st.selectbox("Zona climatica", [
        "no especificada", "humeda", "tropical", "costera",
        "fria", "andina", "patagonica", "seca", "arida", "desertica"
    ])

cerca_del_mar = st.radio(
    "El inmueble esta cerca del mar?",
    ["No", "Si"],
    horizontal=True
)

st.markdown('<div class="seccion-label">Observaciones del tecnico</div>', unsafe_allow_html=True)
observaciones = st.text_area(
    "Notas internas (no se muestran al cliente)",
    placeholder="Ej: Revise la medianera norte. Hay eflorescencias en la base...",
    height=80,
)

st.markdown("<br>", unsafe_allow_html=True)
diagnosticar = st.button("Diagnosticar problema")

if diagnosticar:
    st.toast("Procesando diagnóstico...", icon="⏳")
    st.session_state.primer_uso = False
    if not descripcion.strip():
        st.warning("Por favor describi el problema antes de continuar.")
        st.stop()

    try:
        analisis_imagen = ""
        if fotos:
            from google import genai
            import time 
            from PIL import Image
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            analisis_partes = []
            for foto in fotos:
                imagen = Image.open(foto)
                for intento in range(3):
                    try:
                        respuesta = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=[
                            "Hola. Soy un inspector tecnico edilicio. Analiza la imagen e identifica: tipo de humedad, superficie afectada, nivel de deterioro, manchas, eflorescencia, salitre, hongos, goteras, grietas, oxido o condensacion visible. Respuesta tecnica y precisa, maximo 4 lineas.",
                            imagen
                        ])
                        break
                    except Exception as e:
                        if "429" in str(e) and intento < 2:
                            time.sleep(5)
                        else:
                            raise
    

                analisis_partes.append(respuesta.text)
            analisis_imagen = " | ".join(analisis_partes)
        resultado = clasificar_humedad(
            descripcion=descripcion + " " + analisis_imagen,
            lugar=lugar.lower(),
            zona_climatica=zona_climatica.lower(),
            cerca_del_mar=(cerca_del_mar == "Si")
        )
        st.session_state.diagnosticos_total += 1
        cliente_data = {"nombre": nombre, "direccion": direccion, "telefono": telefono}

        st.markdown("---")

        diagnostico = resultado.get("diagnostico", [])
        if isinstance(diagnostico, dict):
            diagnostico = [diagnostico]

        for item in diagnostico:
            clase = color_clase(item.get("urgencia", "A evaluar"))
            st.markdown(f"""
<div class="resultado-card resultado-{clase}">
  <div class="resultado-titulo">{item.get('categoria', '')}</div>
  <span class="badge-urgencia badge-{clase}">{item.get('urgencia', 'A evaluar')}</span><br>
  <div style="font-size:0.85rem;color:var(--texto-suave);margin-top:0.4rem">{item.get('solucion', '')}</div>
  <div class="resultado-presupuesto">{item.get('presupuesto', 'A determinar')}</div>
</div>
""", unsafe_allow_html=True)
            if item.get("materiales"):
                mats = "".join([f'<div style="color:#F0EBE3;font-size:0.85rem;padding:0.2rem 0">&#8226; {m}</div>' for m in item["materiales"]])
                st.markdown(f'''<div style="margin-top:0.8rem;padding:0.8rem 1rem;background:rgba(15,52,96,0.5);border-radius:8px;border:1px solid rgba(232,108,26,0.2)"><div style="color:#F0EBE3;font-size:0.85rem;font-weight:600;margin-bottom:0.5rem">Materiales recomendados:</div>{mats}</div>''', unsafe_allow_html=True)

        alertas = (
            resultado.get("alertas_zona", []) +
            resultado.get("alertas_lugar", []) +
            resultado.get("alertas_salinidad", [])
        )
        if alertas:
            st.markdown("---")
            st.markdown('<div class="seccion-label">Alertas adicionales</div>', unsafe_allow_html=True)
            for alerta in alertas:
                st.markdown(f'<div class="alerta-item">{alerta}</div>', unsafe_allow_html=True)
        if analisis_imagen:
                st.markdown("---")
                st.markdown('<div class="seccion-label">Lo que detectamos en la imagen</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="alerta-item">{analisis_imagen}</div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:1rem;padding:0.8rem 1rem;background:rgba(232,108,26,0.08);border:1px solid rgba(232,108,26,0.25);border-radius:8px;font-size:0.82rem;color:#C9B99A">⚠️ Este diagnóstico es orientativo y está sujeto a la inspección final del técnico en el lugar.</div>', unsafe_allow_html=True)
        entrada = {
            "hora": datetime.datetime.now().strftime("%H:%M"),
            "nombre": nombre or "Sin nombre",
            "categoria": diagnostico[0].get("categoria", "") if diagnostico else "",
            "urgencia": diagnostico[0].get("urgencia", "") if diagnostico else "",
            "informe": generar_informe(cliente_data, resultado, observaciones),
        }
        st.session_state.historial.insert(0, entrada)
        if len(st.session_state.historial) > 20:
            st.session_state.historial.pop()

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="Descargar informe completo",
            data=entrada["informe"],
            file_name=f"CasaSana_{nombre.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
        )

    except Exception as e:
        st.error("Algo salio mal. Espera unos segundos.")
        with st.expander("Log tecnico"):
            st.code(str(e))

if st.session_state.historial:
    st.markdown("---")
    st.markdown('<div class="seccion-label">Historial de sesion</div>', unsafe_allow_html=True)
    col_h1, col_h2 = st.columns([4, 1])
    with col_h2:
        if st.button("Limpiar", key="limpiar_historial"):
            st.session_state.historial = []
            st.rerun()
    for item in st.session_state.historial:
        clase = color_clase(item["urgencia"])
        st.markdown(f"""
<div class="historial-item">
  <span style="color:var(--texto-suave);font-size:0.72rem">{item['hora']}</span>
  &nbsp;·&nbsp;
  <span style="color:var(--naranja-claro);font-weight:600">{item['nombre']}</span>
  &nbsp;·&nbsp;
  <span>{item['categoria']}</span>
  &nbsp;
  <span class="badge-urgencia badge-{clase}">{item['urgencia']}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  <strong>CasaSana.a.i</strong> · Inteligencia que cuida. Precision que resuelve.<br>
  <span style="font-size:0.68rem;opacity:0.5">v1.0 · Mayo 2026 · Latinoamerica</span>
</div>
""", unsafe_allow_html=True)
