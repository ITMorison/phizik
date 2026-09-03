import streamlit as st

from data_io import seed_demo
from database import get_session, init_db
from ui import apply_theme, header


st.set_page_config(page_title="Eco Pack Analytics", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")
init_db()
session = get_session()
try:
    seed_demo(session)
finally:
    session.close()
apply_theme()
header()

st.markdown('<div class="panel"><div class="eyebrow">Eco Pack Analytics / Digital Lab</div><h2>Биопластик туралы шешімдер деректерге негізделген</h2><p class="muted">Сол жақтағы навигация арқылы аналитикаға, эксперименттерді басқаруға немесе есептер экспортына өтіңіз.</p></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Жүйе модульдері · таңдаңыз</div>', unsafe_allow_html=True)
a, b, c = st.columns(3)
with a:
    st.metric("1", "Аналитика", "MCDA + прогноз")
    if st.button("📊 Ашу", key="open_analytics", use_container_width=True):
        st.switch_page("pages/1_Аналитика.py")
with b:
    st.metric("2", "Эксперименттер", "SQLite ORM")
    if st.button("🧪 Ашу", key="open_experiments", use_container_width=True):
        st.switch_page("pages/2_Управление_экспериментами.py")
with c:
    st.metric("3", "Есептер", "Excel + PDF")
    if st.button("📄 Ашу", key="open_reports", use_container_width=True):
        st.switch_page("pages/3_Экспорт_отчетов.py")
st.info("Демонстрациялық эксперимент бірінші іске қосылғанда автоматты түрде дайындалады.")
