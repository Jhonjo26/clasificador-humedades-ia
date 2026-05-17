 import streamlit as st
from main import clasificar_humedad
import datetime

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CasaSana.a.i",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS INYECTADO ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

  /* ── Variables ── */
  :root {
    --naranja:      #E86C1A;
    --naranja-claro:#E8A87C;
    --oscuro:       #1A1A2E;
    --oscuro-mid:   #16213E;
    --oscuro-card:  #0F3460;
    --texto:        #F0EBE3;
    --texto-suave:  #C9B99A;
    --urgente:      #FF4C4C;
    --alta:         #E86C1A;
    --media:        #F5C518;
    --baja:         #4CAF50;
    --radio:        12px;
  }

  /* ── Reset & Base ── */
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--oscuro) !important;
    color: var(--texto) !important;
  }

  .stApp {
    background: linear-gradient(160deg, #1A1A2E 0%, #0F3460 60%, #16213E 100%) !important;
    min-height: 100vh;
  }

  /* ── Header Hero ── */
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
  .hero-logo span {
    color: var(--naranja-claro);
    font-weight: 400;
    font-size: 1rem;
  }
  .hero-eslogan {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 300;
    color: var(--texto-suave);
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  /* ── Bienvenida EMMA ── */
  .bienvenida-card {
    background: linear-gradient(135deg, rgba(232,108,26,0.15), rgba(232,168,124,0.08));
    border: 1px solid rgba(232,108,26,0.35);
    border-radius: var(--radio);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
  }
  .bienvenida-card::before {
    content: '🏠';
    position: absolute;
    right: 1.2rem;
    top: 1rem;
    font-size: 2.5rem;
    opacity: 0.15;
  }
  .bienvenida-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--naranja);
    margin-bottom: 0.4rem;
  }
  .bienvenida-texto {
    font-size: 0.88rem;
    color: var(--texto-suave);
    line-height: 1.6;
    margin-bottom: 0.8rem;
  }
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

  /* ── Sección Labels ── */
  .seccion-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--naranja);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 1.4rem;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .seccion-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(232,108,26,0.2);
  }

  /* ── Inputs Streamlit ── */
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea,
  .stSelectbox > div > div,
  .stRadio > div {
    background-color: rgba(15, 52, 96, 0.6) !important;
    border: 1px solid rgba(232,108,26,0.3) !important;
    border-radius: var(--radio) !important;
    color: var(--texto) !important;
    font-family: 'DM Sans', sans-serif !important;
  }
  .stTextInput > div > div > input:focus,
  .stTextArea > div > div > textarea:focus {
    border-color: var(--naranja) !important;
    box-shadow: 0 0 0 2px rgba(232,108,26,0.2) !important;
  }
  .stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label {
    color: var(--texto-suave) !important;
    font-size: 0.85rem !important;
  }

  /* ── Botón Principal ── */
  .stButton > button {
    background: linear-gradient(135deg, var(--naranja), #C4571A) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radio) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.7rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(232,108,26,0.35) !important;
  }
  .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(232,108,26,0.5) !important;
  }
  .stButton > button:active {
    transform: translateY(0) !important;
  }

  /* ── Resultado Card ── */
  .resultado-card {
    border-radius: var(--radio);
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
    border-left: 4px solid;
    position: relative;
  }
  .resultado-urgente {
    background: rgba(255,76,76,0.1);
    border-color: var(--urgente);
  }
  .resultado-alta {
    background: rgba(232,108,26,0.12);
    border-color: var(--alta);
  }
  .resultado-media {
    background: rgba(245,197,24,0.1);
    border-color: var(--media);
  }
  .resultado-baja {
    background: rgba(76,175,80,0.1);
    border-color: var(--baja);
  }
  .resultado-id {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    color: var(--texto-suave);
    text-transform: uppercase;
    margin-bottom: 0.3rem;
  }
  .resultado-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--texto);
    margin-bottom: 0.6rem;
  }
  .badge-urgencia {
    display: inline-block;
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
  }
  .badge-urgente  { background: rgba(255,76,76,0.25);  color: #FF8080; }
  .badge-alta     { background: rgba(232,108,26,0.25); color: var(--naranja-claro); }
  .badge-media    { background: rgba(245,197,24,0.2);  color: #F5E06A; }
  .badge-baja     { background: rgba(76,175,80,0.2);   color: #80C883; }
  .badge-evaluar  { background: rgba(150,150,150,0.2); color: #AAAAAA; }

  .resultado-detalle {
    font-size: 0.85rem;
    color: var(--texto-suave);
    line-height: 1.6;
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
    margin-top: 0.8rem;
  }

  /* ── Error Empático ── */
  .error-card {
    background: rgba(255,76,76,0.08);
    border: 1px solid rgba(255,76,76,0.3);
    border-radius: var(--radio);
    padding: 1.2rem 1.4rem;
    margin: 0.8rem 0;
  }
  .error-aviso {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: #FF8080;
    margin-bottom: 0.3rem;
  }
  .error-contexto {
    font-size: 0.82rem;
    color: var(--texto-suave);
    margin-bottom: 0.5rem;
  }
  .error-solucion {
    font-size: 0.82rem;
    color: var(--naranja-claro);
    font-weight: 500;
  }

  /* ── Historial ── */
  .historial-item {
    background: rgba(15, 52, 96, 0.4);
    border: 1px solid rgba(232,108,26,0.15);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.82rem;
  }
  .historial-hora {
    color: var(--texto-suave);
    font-size: 0.72rem;
    margin-bottom: 0.2rem;
  }
  .historial-nombre {
    font-weight: 600;
    color: var(--naranja-claro);
  }

  /* ── Footer ── */
  .footer {
    text-align: center;
    padding: 2rem 1rem 1rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(232,108,26,0.15);
    font-size: 0.75rem;
    color: var(--texto-suave);
  }
  .footer strong { color: var(--naranja); }

  /* ── Contador diagnósticos ── */
  .contador-badge {
    background: rgba(232,108,26,0.2);
    border: 1px solid rgba(232,108,26,0.35);
    border-radius: 20px;
    padding: 0.3rem 1rem;
    font-size: 0.78rem;
    color: var(--naranja-claro);
    text-align: center;
    margin-bottom: 1.5rem;
    display: inline-block;
  }

  /* ── Divider ── */
  hr {
    border: none !important;
    border-top: 1px solid rgba(232,108,26,0.2) !important;
    margin: 1.5rem 0 !important;
  }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: var(--oscuro); }
  ::-webkit-scrollbar-thumb { background: var(--naranja); border-radius: 2px; }

  /* ── Ocultar elementos Streamlit ── */
  #MainMenu { visibility: hidden; }
  footer { visibility: hidden; }
  header { visibility: hidden; }
  .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "historial" not in st.session_state:
    st.session_state.historial = []
if "diagnosticos_total" not in st.session_state:
    st.session_state.diagnosticos_total = 0
if "primer_uso" not in st.session_state:
    st.session_state.primer_uso = True


# ── HELPERS ───────────────────────────────────────────────────────────────────
def color_clase(urgencia: str) -> str:
    u = urgencia.lower()
    if "urgente" in u:   return "urgente"
    if "alta" in u:      return "alta"
    if "media" in u:     return "media"
    if "baja" in u:      return "baja"
    return "evaluar"


def badge_html(urgencia: str) -> str:
    clase = color_clase(urgencia)
    return f'<span class="badge-urgencia badge-{clase}">{urgencia}</span>'


def generar_informe(cliente, resultados, observaciones):
    lineas = [
        "=" * 48,
        "         INFORME CASASANA.A.I",
        "  Inteligencia que cuida. Precisión que resuelve.",
        "=" * 48,
        f"Cliente   : {cliente.get('nombre','—')}",
        f"Dirección : {cliente.get('direccion','—')}",
        f"Teléfono  : {cliente.get('telefono','—')}",
        f"Fecha     : {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "=" * 48,
    ]
    for i, r in enumerate(resultados, 1):
        lineas += [
            f"\nDIAGNÓSTICO {i}: {r.get('categoria','—')}  [{r.get('id','—')}]",
            f"Urgencia   : {r.get('urgencia','—')}",
            f"Presupuesto: {r.get('presupuesto','—')}",
        ]
        if r.get("alertas"):
            for a in r["alertas"]:
                lineas.append(f"⚠  {a}")
    if observaciones:
        lineas += ["\n" + "─" * 48, "OBSERVACIONES DEL TÉCNICO:", observaciones]
    lineas += ["", "=" * 48, "CasaSana.a.i  —  casasana.ai"]
    return "\n".join(lineas)


# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-logo">CasaSana<span>.a.i</span></div>
  <div class="hero-eslogan">Inteligencia que cuida · Precisión que resuelve</div>
</div>
""", unsafe_allow_html=True)


# ── BIENVENIDA EMMA (Educar + Hospitalidad = Aha! Moment) ────────────────────
if st.session_state.primer_uso:
    st.markdown("""
<div class="bienvenida-card">
  <div class="bienvenida-titulo">👋 Bienvenido a CasaSana.a.i</div>
  <div class="bienvenida-texto">
    Describí el problema de humedad de tu cliente con tus propias palabras
    y en segundos recibís un diagnóstico con categoría, urgencia y presupuesto estimado.
    Sin formularios complicados. Sin espera.
  </div>
  <span class="bienvenida-beneficio">⚡ Diagnóstico instantáneo</span>
  <span class="bienvenida-beneficio">💰 Presupuesto estimado</span>
  <span class="bienvenida-beneficio">📋 Informe descargable</span>
</div>
""", unsafe_allow_html=True)


# ── CONTADOR DE CONFIANZA ─────────────────────────────────────────────────────
total = st.session_state.diagnosticos_total
if total > 0:
    st.markdown(
        f'<div style="text-align:center"><span class="contador-badge">'
        f'✅ {total} diagnóstico{"s" if total != 1 else ""} realizados en esta sesión'
        f'</span></div>',
        unsafe_allow_html=True
    )


# ── DATOS DEL CLIENTE ─────────────────────────────────────────────────────────
st.markdown('<div class="seccion-label">Datos del cliente</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])
with col1:
    nombre = st.text_input("Nombre completo", placeholder="Ej: María González")
with col2:
    telefono = st.text_input("Teléfono", placeholder="Ej: 11-4567-8900")

direccion = st.text_input("Dirección del inmueble", placeholder="Ej: Av. Corrientes 1234, CABA")


# ── DESCRIPCIÓN DEL PROBLEMA ──────────────────────────────────────────────────
st.markdown('<div class="seccion-label">Descripción del problema</div>', unsafe_allow_html=True)

descripcion = st.text_area(
    "Describí el problema con tus palabras",
    placeholder="Ej: Hay manchas de humedad en el techo del baño y el piso se está levantando. El olor es muy fuerte...",
    height=110,
)


# ── SELECTORES ────────────────────────────────────────────────────────────────
st.markdown('<div class="seccion-label">Contexto del inmueble</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    lugar = st.selectbox("Lugar físico afectado", [
        "no_especificado", "techo", "sotano", "pared exterior",
        "pared interior", "piso", "cocina", "baño",
        "jardin", "garage", "terraza"
    ])
with col4:
    zona = st.selectbox("Zona climática", [
        "no_especificada", "humeda", "seca", "fria",
        "templada", "tropical", "costera", "montana",
        "semiarida", "mediterranea"
    ])

mar = st.radio(
    "¿El inmueble está cerca del mar?",
    ["no", "si"],
    horizontal=True
)


# ── OBSERVACIONES ─────────────────────────────────────────────────────────────
st.markdown('<div class="seccion-label">Observaciones del técnico</div>', unsafe_allow_html=True)

observaciones = st.text_area(
    "Notas internas (no se muestran al cliente)",
    placeholder="Ej: Revisé la medianera norte. Hay eflorescencias en la base...",
    height=80,
)


# ── BOTÓN DIAGNOSTICAR ────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
diagnosticar = st.button("🔍 Diagnosticar problema")


# ── LÓGICA PRINCIPAL ──────────────────────────────────────────────────────────
if diagnosticar:
    st.session_state.primer_uso = False

    # ── Validación empática ──
    errores = []
    if not nombre.strip():
        errores.append(("nombre", "Falta el nombre del cliente", "Completá el campo Nombre completo."))
    if not descripcion.strip():
        errores.append(("descripcion", "Falta describir el problema", "Contanos qué está pasando con el inmueble."))

    if errores:
        for _, aviso, solucion in errores:
            st.markdown(f"""
<div class="error-card">
  <div class="error-aviso">⚠ {aviso}</div>
  <div class="error-contexto">Para darte un diagnóstico preciso necesitamos un dato más.</div>
  <div class="error-solucion">→ {solucion}</div>
</div>
""", unsafe_allow_html=True)
        st.stop()

    # ── Clasificación ──
    try:
        resultados = clasificar_humedad(
            descripcion=descripcion,
            lugar=lugar,
            zona=zona,
            mar=(mar == "si"),
        )

        if not resultados:
            st.markdown("""
<div class="error-card">
  <div class="error-aviso">🔎 No pudimos identificar el problema</div>
  <div class="error-contexto">La descripción no coincidió con nuestras categorías conocidas.</div>
  <div class="error-solucion">→ Agregá más detalles: ¿dónde aparece? ¿desde cuándo? ¿hay olor?</div>
</div>
""", unsafe_allow_html=True)
            st.stop()

        # ── Mostrar resultados ──
        st.session_state.diagnosticos_total += 1
        cliente_data = {"nombre": nombre, "direccion": direccion, "telefono": telefono}

        st.markdown("---")
        st.markdown(f"""
<div style="font-family:'Syne',sans-serif; font-size:0.72rem; color:var(--texto-suave,#C9B99A);
     text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.8rem;">
  ✅ Diagnóstico para <strong style="color:#E8A87C">{nombre}</strong>
</div>
""", unsafe_allow_html=True)

        for r in resultados:
            clase = color_clase(r.get("urgencia", ""))
            alertas_html = ""
            if r.get("alertas"):
                alertas_items = "".join([f"<li>{a}</li>" for a in r["alertas"]])
                alertas_html = f"""
<div style="margin-top:0.8rem; padding:0.6rem 0.8rem; background:rgba(232,108,26,0.1);
     border-radius:8px; font-size:0.8rem; color:#E8A87C;">
  <strong>⚠ Alertas contextuales:</strong>
  <ul style="margin:0.3rem 0 0 1rem; padding:0;">{alertas_items}</ul>
</div>"""

            st.markdown(f"""
<div class="resultado-card resultado-{clase}">
  <div class="resultado-id">{r.get('id','—')}</div>
  <div class="resultado-titulo">{r.get('categoria','—')}</div>
  {badge_html(r.get('urgencia','—'))}
  <div class="resultado-detalle">{r.get('descripcion', '')}</div>
  <div class="resultado-presupuesto">💰 {r.get('presupuesto','A determinar')}</div>
  {alertas_html}
</div>
""", unsafe_allow_html=True)

        # ── Guardar en historial ──
        entrada = {
            "hora": datetime.datetime.now().strftime("%H:%M"),
            "nombre": nombre,
            "categoria": resultados[0].get("categoria", "—"),
            "urgencia": resultados[0].get("urgencia", "—"),
            "informe": generar_informe(cliente_data, resultados, observaciones),
        }
        st.session_state.historial.insert(0, entrada)
        if len(st.session_state.historial) > 20:
            st.session_state.historial.pop()

        # ── Descarga ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📄 Descargar informe completo",
            data=entrada["informe"],
            file_name=f"CasaSana_{nombre.replace(' ','_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
        )

    except Exception as e:
        st.markdown(f"""
<div class="error-card">
  <div class="error-aviso">⚙ Algo salió mal en el sistema</div>
  <div class="error-contexto">Ocurrió un error inesperado al procesar el diagnóstico. Ya lo registramos.</div>
  <div class="error-solucion">→ Intentá de nuevo en unos segundos. Si persiste, contactá soporte.</div>
</div>
""", unsafe_allow_html=True)
        # Log técnico (no visible al cliente)
        with st.expander("🔧 Log técnico (solo técnicos)"):
            st.code(str(e))


# ── HISTORIAL ─────────────────────────────────────────────────────────────────
if st.session_state.historial:
    st.markdown("---")
    st.markdown('<div class="seccion-label">Historial de sesión</div>', unsafe_allow_html=True)

    col_h1, col_h2 = st.columns([4, 1])
    with col_h2:
        if st.button("🗑 Limpiar", key="limpiar_historial"):
            st.session_state.historial = []
            st.rerun()

    for item in st.session_state.historial:
        clase = color_clase(item["urgencia"])
        st.markdown(f"""
<div class="historial-item">
  <div class="historial-hora">🕐 {item['hora']}</div>
  <span class="historial-nombre">{item['nombre']}</span>
  &nbsp;·&nbsp;
  <span style="font-size:0.82rem; color:var(--texto,#F0EBE3)">{item['categoria']}</span>
  &nbsp;
  <span class="badge-urgencia badge-{clase}" style="font-size:0.7rem">{item['urgencia']}</span>
</div>
""", unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <strong>CasaSana.a.i</strong> · Inteligencia que cuida. Precisión que resuelve.<br>
  <span style="font-size:0.68rem; opacity:0.5; margin-top:0.3rem; display:block;">
    v1.0 · Mayo 2026 · Latinoamérica
  </span>
</div>
""", unsafe_allow_html=True)
