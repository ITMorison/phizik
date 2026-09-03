import streamlit as st
from sqlalchemy import delete

from analytics import CRITERIA
from data_io import DAYS, import_frame, parse_upload, frame_template
from database import get_session, init_db
from models import Experiment, MassMeasurement, QualityCriteria, Sample
from ui import apply_theme, header

init_db(); apply_theme(); header(); st.header("Басқару экспериментами")
session = get_session()
try:
    st.subheader("Импорт лабораторных данных")
    st.download_button("Скачать шаблон Excel", frame_template().to_csv(index=False).encode("utf-8-sig"), "ecopack_template.csv", "text/csv")
    uploaded = st.file_uploader("Загрузить XLSX или CSV", type=["xlsx", "csv"])
    if uploaded and st.button("Импортировать в БД", type="primary"):
        try:
            count = import_frame(session, parse_upload(uploaded))
            st.success(f"Импортировано образцов: {count}")
        except (ValueError, OSError) as error:
            st.error(str(error))
    experiments = session.query(Experiment).order_by(Experiment.id.desc()).all()
    for experiment in experiments:
        with st.expander(f"#{experiment.id} · {experiment.name} · {experiment.author}"):
            st.write(experiment.description or "Описание не задано")
            for sample in experiment.samples:
                quality = sample.quality
                values = {"Образец": sample.name, "Состав": sample.composition, **{label: getattr(quality, field) for label, field in CRITERIA.items()}}
                st.dataframe([values], width="stretch", hide_index=True)
            if st.button("Удалить эксперимент", key=f"delete_{experiment.id}"):
                session.delete(experiment); session.commit(); st.rerun()
    st.subheader("Ручное добавление")
    with st.form("manual"):
        name = st.text_input("Название эксперимента", "Новый эксперимент")
        author = st.text_input("Автор", "Eco Pack Lab")
        sample_name = st.text_input("Название образца", "5-үлгі")
        composition = st.text_input("Состав", "Крахмал 50%, глицерин 15%")
        quality_values = [st.number_input(criterion, min_value=0.0, max_value=100.0, value=50.0) for criterion in CRITERIA]
        masses = [st.number_input(f"Масса, день {day}", min_value=0.0, value=20.0) for day in DAYS]
        submitted = st.form_submit_button("Сохранить образец")
    if submitted:
        experiment = Experiment(name=name, author=author, description="Введено вручную")
        session.add(experiment); session.flush()
        sample = Sample(experiment_id=experiment.id, name=sample_name, composition=composition)
        session.add(sample); session.flush()
        quality_data = {
            field: value
            for (label, field), value in zip(CRITERIA.items(), quality_values)
        }
        session.add(QualityCriteria(sample_id=sample.id, **quality_data))
        session.add_all([MassMeasurement(sample_id=sample.id, day=day, mass=mass) for day, mass in zip(DAYS, masses)])
        session.commit(); st.success("Образец сохранен в SQLite."); st.rerun()
finally:
    session.close()
