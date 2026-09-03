from io import BytesIO
import pandas as pd
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from analytics import CRITERIA, DEFAULT_WEIGHTS, normalize_and_score, recommendation
from database import get_session, init_db
from models import Experiment
from ui import apply_theme, header

init_db(); apply_theme(); header(); st.header("Экспорт отчетов")
session = get_session()
try:
    experiments = session.query(Experiment).order_by(Experiment.id.desc()).all()
    if not experiments:
        st.info("Нет экспериментов для отчета."); st.stop()
    selected_id = st.selectbox("Выберите эксперимент", [item.id for item in experiments], format_func=lambda value: next(item.name for item in experiments if item.id == value))
    experiment = session.get(Experiment, selected_id)
    rows = [{"Образец": sample.name, **{label: getattr(sample.quality, field) for label, field in CRITERIA.items()}} for sample in experiment.samples]
    criteria = pd.DataFrame(rows).set_index("Образец")
    scores = normalize_and_score(criteria, DEFAULT_WEIGHTS)
    compositions = {sample.name: sample.composition for sample in experiment.samples}
    winner, score, explanation = recommendation(scores, compositions)
    st.success(explanation)
    excel = BytesIO()
    with pd.ExcelWriter(excel, engine="openpyxl") as writer:
        scores.to_excel(writer, sheet_name="Аналитика")
        criteria.to_excel(writer, sheet_name="Критерии")
    st.download_button("Скачать Excel-отчет", excel.getvalue(), f"ecopack_report_{experiment.id}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    pdf = BytesIO(); document = canvas.Canvas(pdf, pagesize=A4)
    document.setFont("Helvetica-Bold", 18); document.drawString(48, 790, "Eco Pack Analytics")
    document.setFont("Helvetica", 11); document.drawString(48, 765, f"Эксперимент: {experiment.name}")
    document.drawString(48, 745, f"Рекомендация: {winner}, оценка {score:.2f}/1.00")
    text = document.beginText(48, 715); text.setFont("Helvetica", 10)
    for line in explanation[:220].split(". "):
        text.textLine(line); 
    document.drawText(text); document.save(); pdf.seek(0)
    st.download_button("Скачать PDF-отчет", pdf.getvalue(), f"ecopack_report_{experiment.id}.pdf", "application/pdf")
finally:
    session.close()
