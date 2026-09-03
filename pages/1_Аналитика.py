import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from analytics import CRITERIA, DAYS, DEFAULT_WEIGHTS, forecast_mass, normalize_and_score, recommendation
from database import get_session, init_db
from models import MassMeasurement, QualityCriteria, Sample
from ui import apply_theme, header

init_db(); apply_theme(); header()
session = get_session()
try:
    samples = session.query(Sample).all()
    if not samples:
        st.warning("Нет данных. Откройте страницу управления экспериментами и добавьте исследование.")
        st.stop()
    selected = st.sidebar.multiselect("Үлгілерді салыстыру", [s.name for s in samples], default=[s.name for s in samples])
    weights = [st.sidebar.slider(label, 0.0, 1.0, value=value, step=0.05) for label, value in zip(CRITERIA, DEFAULT_WEIGHTS)]
    total = sum(weights) or 1
    weights = [value / total for value in weights]
    rows, compositions, mass_map = [], {}, {}
    for sample in samples:
        quality = sample.quality
        rows.append({"Үлгі": sample.name, **{label: getattr(quality, field) for label, field in CRITERIA.items()}})
        compositions[sample.name] = sample.composition
        mass_map[sample.name] = sorted(sample.mass_measurements, key=lambda item: item.day)
    criteria = pd.DataFrame(rows).set_index("Үлгі")
    scores = normalize_and_score(criteria, weights)
    winner, winner_score, explanation = recommendation(scores, compositions)
    average_strength = float(criteria["Беріктік"].mean())
    best_bio = float(criteria["Биоыдырау"].max())
    st.markdown(f'<div class="ai-panel"><div class="kpi-label">AI ұсынған ең тиімді үлгі</div><div class="ring">{winner.upper()}</div><b>{winner_score:.2f} / 1.00</b><div class="muted">{explanation}</div></div>', unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)
    k1.metric("Ең тиімді үлгі", winner, f"{winner_score:.2f}")
    k2.metric("Ең жоғары биоыдырау", f"{best_bio:.0f}/100")
    k3.metric("Орташа беріктік", f"{average_strength:.1f}/100")
    visible = [name for name in selected if name in scores.index] or list(scores.index)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Критерийлер профилі")
        fig = go.Figure()
        criteria_labels = list(CRITERIA)
        for name in visible:
            values = scores.loc[name, criteria_labels].tolist()
            fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=criteria_labels + [criteria_labels[0]], fill="toself", name=name))
        fig.update_layout(template="plotly_dark", height=390, polar={"radialaxis": {"range": [0, 1]}}, margin={"t": 20, "b": 20})
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    with c2:
        st.subheader("Масса және 60 күндік прогноз")
        fig = go.Figure()
        for name in visible:
            measurements = mass_map[name]
            forecast = forecast_mass([m.day for m in measurements], [m.mass for m in measurements])
            for kind, part in forecast.groupby("kind"):
                fig.add_trace(go.Scatter(x=part.day, y=part.mass, mode="lines+markers" if kind == "Факт" else "lines", name=f"{name} · {kind}"))
        fig.update_layout(template="plotly_dark", height=390, xaxis_title="Күн", yaxis_title="Масса, г", margin={"t": 20, "b": 35})
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.subheader("Итоговые баллы по критериям")
    fig = go.Figure()
    for criterion in CRITERIA:
        fig.add_trace(go.Bar(x=scores.index, y=scores[criterion], name=criterion))
    fig.add_trace(go.Scatter(x=scores.index, y=scores["Жалпы баға"], mode="lines+markers", name="Жалпы баға", line={"color": "white", "dash": "dot"}))
    fig.update_layout(template="plotly_dark", barmode="group", height=360, yaxis={"range": [0, 1.15]})
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
finally:
    session.close()
