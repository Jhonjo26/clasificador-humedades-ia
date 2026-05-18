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
    font-size: 2.4rem;
    font-weight: 800;
    color: var(--naranja);
    letter-spacing: -0.5px;
    line-height: 1;
    margin-bottom: 0.3rem;
  }
  .hero-logo span { color: var(--naranja-claro); font-weight: 400; font-size: 1rem; }
  .hero-eslogan {
    font-family: 'DM Sans', sans-serif;
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
    position: relative;
    overflow: hidden;
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
  .stButton > button {
    background: linear-gradient(135deg, var(--naranja), #C4571A) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radio) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    width: 100% !important;
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
  .resultado-id { font-size: 0.65rem; color: var(--texto-suave); text-transform: uppercase; letter-spacing: 0.15em; }
  .resultado-titulo { font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 700; color: var(--texto); margin-bottom: 0.6rem; }
  .badge-urgencia { display: inline-block; border-radius: 20px; padding: 0.2rem 0.75rem; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.8rem; }
  .badge-urgente { background: rgba(255,76,76,0.25); color: #FF8080; }
  .badge-alta { background: rgba(232,108,26,0.25); color: var(--naranja-claro); }
  .badge-media { background: rgba(245,197,24,0.2); color: #F5E06A; }
  .badge-baja { background: rgba(76,175,80,0.2); color: #80C883; }
  .badge-evaluar { background: rgba(150,150,150,0.2); color: #AAAAAA; }
  .resultado-detalle { font-size: 0.85rem; color: var(--texto-suave); line-height: 1.6; }
  .resultado-presupuesto {
    display: inline-block;
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--naranja-claro);
    background: rgba(232,108,26,0.15);
    border-radius: 8px;
    padding: 0.3rem 0.8rem;
    margin-top: 0.8rem;
  }
  .error-card {
    background: rgba(255,76,76,0.08);
    border: 1px solid rgba(255,76,76,0.3);
    border-radius: var(--radio);
    padding: 1.2rem 1.4rem;
    margin: 0.8rem 0;
  }
  .error-aviso { font-family: 'Syne', sans-serif; font-size: 0.9rem; font-weight: 700; color: #FF8080; margin-bottom: 0.3rem; }
  .error-contexto { font-size: 0.82rem; color: var(--texto-suave); margin-bottom: 0.5rem; }
  .error-solucion { font-size: 0.82rem; color: var(--naranja-claro); font-weight: 500; }
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
</style>
""", unsafe_allow_html=True)

if "historial" not in st.session_state:
    st.session_state.historial = []
if "diagnosticos_total" not in st.session_state:
    st.session_state.diagnosticos_total = 0
if "primer_uso" not in st.session_state:
    st.session_state.primer_uso = True


def color_clase(urgencia):
    u = urgencia.lower()
    if "urgente" in u:
        return "urgente"
    if "alta" in u:
        return "alta"
    if "media" in u:
        return "media"
    if "baja" in u:
        return "baja"
    return "evaluar"


def badge_html(urgencia):
    clase = color_clase(urgencia)
    return f'<span class="badge-urgencia badge-{clase}">{urgencia}</span>'


def generar_informe(cliente, resultados, observaciones):
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
    ]
    for i, r in enumerate(resultados, 1):
        lineas += [
            f"\nDIAGNOSTICO {i}: {r.get('categoria', '')}",
            f"Urgencia   : {r.get('urgencia', '')}",
            f"Presupuesto: {r.get('presupuesto', '')}",
        ]
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
    Describi el problema de humedad de tu cliente con tus propias palabras
    y en segundos recibes un diagnostico con categoria, urgencia y presupuesto estimado.
  </div>
  <span class="bienvenida-beneficio">Diagnostico instantaneo</span>
  <span class="bienvenida-beneficio">Presupuesto estimado</span>
  <span class="bienvenida-beneficio">Informe descargable</span>
</div>
""", unsafe_allow_html=True)

total = st.session_state.diagnosticos_total
if total > 0:
    st.info(f"Diagnosticos realizados en esta sesion: {total}")

st.markdown('<div class="seccion-label">Datos del cliente</div>', unsafe_allow_html=True)
col1, col2 = st.columns([3, 2])
with col1:
    nombre = st.text_input("Nombre completo", placeholder="Ej: Maria Gonzalez")
with col2:
    telefono = st.text_input("Telefono", placeholder="Ej: 11-4567-8900")
direccion = st.text_input("Direccion del inmueble", placeholder="Ej: Av. Corrientes 1234, CABA")

st.markdown('<div class="seccion-label">Descripcion del problema</div>', unsafe_allow_html=True)
descripcion = st.text_area(
    "Describi el problema con tus palabras",
    placeholder="Ej: Hay manchas de humedad en el techo del bano y el piso se esta levantando...",
    height=110,
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
    st.session_state.primer_uso = False
    errores = []
    if not nombre.strip():
        errores.append("Falta el nombre del cliente.")
    if not descripcion.strip():
        errores.append("Falta describir el problema.")
    if errores:
        for e in errores:
            st.markdown(f"""
<div class="error-card">
  <div class="error-aviso">Falta un dato</div>
  <div class="error-contexto">Para darte un diagnostico preciso necesitamos un dato mas.</div>
  <div class="error-solucion">{e}</div>
</div>
""", unsafe_allow_html=True)
        st.stop()
    try:
        resultados = clasificar_humedad(descripcion)
        if not resultados:
            st.markdown("""
<div class="error-card">
  <div class="error-aviso">No pudimos identificar el problema</div>
  <div class="error-contexto">La descripcion no coincidio con nuestras categorias conocidas.</div>
  <div class="error-solucion">Agrega mas detalles: donde aparece, desde cuando, hay olor?</div>
</div>
""", unsafe_allow_html=True)
            st.stop()
        st.session_state.diagnosticos_total += 1
        cliente_data = {"nombre": nombre, "direccion": direccion, "telefono": telefono}
        st.markdown("---")
        for r in resultados:
            clase = color_clase(r.get("urgencia", ""))
            st.markdown(f"""
<div class="resultado-card resultado-{clase}">
  <div class="resultado-id">{r.get('id', '')}</div>
  <div class="resultado-titulo">{r.get('categoria', '')}</div>
  {badge_html(r.get('urgencia', ''))}
  <div class="resultado-detalle">{r.get('descripcion', '')}</div>
  <div class="resultado-presupuesto">{r.get('presupuesto', 'A determinar')}</div>
</div>
""", unsafe_allow_html=True)
        entrada = {
            "hora": datetime.datetime.now().strftime("%H:%M"),
            "nombre": nombre,
            "categoria": resultados[0].get("categoria", ""),
            "urgencia": resultados[0].get("urgencia", ""),
            "informe": generar_informe(cliente_data, resultados, observaciones),
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
        st.markdown("""
<div class="error-card">
  <div class="error-aviso">Algo salio mal en el sistema</div>
  <div class="error-contexto">Ocurrio un error inesperado. Intentalo de nuevo.</div>
  <div class="error-solucion">Si persiste, contacta soporte.</div>
</div>
""", unsafe_allow_html=True)
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
