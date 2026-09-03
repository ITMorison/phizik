import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');
    :root { --bg:#07110d; --panel:#10231a; --line:#2a4d3a; --mint:#69e6a4; --lime:#c7f36b; --muted:#9ab4a2; }
    .stApp { background: radial-gradient(circle at 90% 0%, #1c422c 0, var(--bg) 38%); font-family:Manrope,sans-serif; }
    [data-testid="stSidebar"] { background:#0b1b13; border-right:1px solid var(--line); }
    h1,h2,h3 { font-family:'Space Grotesk',sans-serif!important; letter-spacing:0!important; }
    h1 { font-size:clamp(2rem,4vw,3.8rem)!important; line-height:1!important; }
    .eyebrow,.section-label { color:var(--lime); font-size:.74rem; font-weight:800; letter-spacing:.1em; text-transform:uppercase; }
    .section-label { color:var(--muted); margin:1.3rem 0 .55rem; }
    .panel { background:rgba(13,31,22,.8); border:1px solid var(--line); border-radius:8px; padding:1rem; }
    .kpi { background:linear-gradient(145deg,#1a4930,#10241a); border:1px solid #4e9561; border-radius:8px; padding:1rem; min-height:125px; }
    .kpi-label { color:#a9c4b0; font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; }
    .kpi-value { color:var(--lime); font:700 2.2rem 'Space Grotesk'; margin:.3rem 0; }
    .muted { color:var(--muted); font-size:.82rem; }
    .step-grid { display:grid; grid-template-columns:repeat(6,1fr); gap:.5rem; margin:1rem 0; }
    .step { background:linear-gradient(145deg,#18382a,#0e2118); border:1px solid var(--line); border-radius:7px; padding:.7rem .3rem; text-align:center; min-height:76px; }
    .step-icon { font-size:1.4rem; }.step-title { font-size:.68rem; font-weight:800; text-transform:uppercase; line-height:1.15; margin-top:.35rem; }
    .ai-panel { background:radial-gradient(circle,#2b6336,#102419 70%); border:1px solid #6fce6c; border-radius:8px; text-align:center; padding:.8rem; }
    .ring { width:76px;height:76px;border:3px solid var(--lime);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:.5rem auto;color:var(--lime);font-weight:800;box-shadow:0 0 18px #91d86666; }
    @media(max-width:850px){.step-grid{grid-template-columns:repeat(3,1fr)}}
    </style>
    """, unsafe_allow_html=True)


def header():
    st.markdown('<div class="eyebrow">Digital biology / sustainability intelligence</div>', unsafe_allow_html=True)
    st.title("ПРОГРАММАЛАУ + AI = ECO PACK ИННОВАЦИЯСЫ")
    st.markdown('<p class="muted">Цифровая лаборатория для анализа, мониторинга и выбора оптимального состава биопластика.</p>', unsafe_allow_html=True)
    st.markdown('<div class="step-grid"><div class="step"><div class="step-icon">🌽</div><div class="step-title">Шикізат</div></div><div class="step"><div class="step-icon">▧</div><div class="step-title">Биопластик</div></div><div class="step"><div class="step-icon">⚗</div><div class="step-title">Деректер</div></div><div class="step"><div class="step-icon">⌘</div><div class="step-title">Python + AI</div></div><div class="step"><div class="step-icon">✣</div><div class="step-title">Оңтайлы құрам</div></div><div class="step"><div class="step-icon">▤</div><div class="step-title">EcoPack</div></div></div>', unsafe_allow_html=True)
    nav_home, nav_analytics, nav_experiments, nav_reports = st.columns(4)
    if nav_home.button("🏠 Басты бет", use_container_width=True):
        st.switch_page("app.py")
    if nav_analytics.button("📊 Аналитика", use_container_width=True):
        st.switch_page("pages/1_Аналитика.py")
    if nav_experiments.button("🧪 Эксперименттер", use_container_width=True):
        st.switch_page("pages/2_Управление_экспериментами.py")
    if nav_reports.button("📄 Есептер", use_container_width=True):
        st.switch_page("pages/3_Экспорт_отчетов.py")
