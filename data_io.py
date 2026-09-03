from __future__ import annotations

from datetime import date
import io
import pandas as pd

from models import Experiment, MassMeasurement, QualityCriteria, Sample

DAYS = [1, 3, 5, 7, 10, 14]
CRITERIA = ["flexibility", "strength", "water_resistance", "water_stability", "biodegradability"]


def demo_rows():
    quality = [[55, 60, 50, 58, 62], [68, 73, 66, 70, 75], [84, 98, 93, 91, 97], [90, 95, 92, 94, 94]]
    masses = [[20, 17.8, 15.4, 12.9, 9.8, 6.7], [20, 18.7, 17, 15, 12.8, 10.5], [20, 19.3, 18.4, 17.2, 15.8, 14.2], [20, 19.6, 19, 18.3, 17.5, 16.8]]
    return [{"name": f"{i + 1}-үлгі", "composition": f"Крахмал {45 + i * 5}%, глицерин {12 + i * 2}%, целлюлоза {10 + i}%", "quality": quality[i], "mass": masses[i]} for i in range(4)]


def seed_demo(session):
    if session.query(Experiment).count():
        return
    experiment = Experiment(name="Eco Pack baseline 2026", experiment_date=date.today(), author="Eco Pack Lab", description="Базовое лабораторное исследование биопластика.")
    session.add(experiment)
    session.flush()
    for row in demo_rows():
        sample = Sample(experiment_id=experiment.id, name=row["name"], composition=row["composition"])
        session.add(sample)
        session.flush()
        session.add(QualityCriteria(sample_id=sample.id, **dict(zip(CRITERIA, row["quality"]))))
        session.add_all([MassMeasurement(sample_id=sample.id, day=day, mass=mass) for day, mass in zip(DAYS, row["mass"])])
    session.commit()


def validate_frame(frame: pd.DataFrame):
    required = {"experiment", "sample", "composition", *CRITERIA, *(f"mass_{day}" for day in DAYS)}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Отсутствуют столбцы: {', '.join(sorted(missing))}")
    numeric = CRITERIA + [f"mass_{day}" for day in DAYS]
    for column in numeric:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if frame[numeric].isna().any().any():
        raise ValueError("В числовых полях найдены пропуски или некорректные типы.")
    if (frame[numeric] < 0).any().any():
        raise ValueError("Значения критериев и массы не могут быть отрицательными.")
    return frame


def parse_upload(uploaded_file) -> pd.DataFrame:
    raw = uploaded_file.getvalue()
    frame = pd.read_excel(io.BytesIO(raw)) if uploaded_file.name.lower().endswith(".xlsx") else pd.read_csv(io.BytesIO(raw))
    return validate_frame(frame)


def import_frame(session, frame: pd.DataFrame, author: str = "Импорт лаборатории") -> int:
    frame = validate_frame(frame.copy())
    grouped = 0
    for experiment_name, group in frame.groupby("experiment"):
        experiment = Experiment(name=str(experiment_name), experiment_date=date.today(), author=author, description="Импортированная лабораторная серия")
        session.add(experiment)
        session.flush()
        for _, row in group.iterrows():
            sample = Sample(experiment_id=experiment.id, name=str(row["sample"]), composition=str(row["composition"]))
            session.add(sample)
            session.flush()
            session.add(QualityCriteria(sample_id=sample.id, **{key: float(row[key]) for key in CRITERIA}))
            session.add_all([MassMeasurement(sample_id=sample.id, day=day, mass=float(row[f"mass_{day}"])) for day in DAYS])
            grouped += 1
    session.commit()
    return grouped


def frame_template() -> pd.DataFrame:
    rows = []
    for row in demo_rows():
        values = {"experiment": "Новый эксперимент", "sample": row["name"], "composition": row["composition"]}
        values.update(dict(zip(CRITERIA, row["quality"])))
        values.update({f"mass_{day}": mass for day, mass in zip(DAYS, row["mass"])})
        rows.append(values)
    return pd.DataFrame(rows)
