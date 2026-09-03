from fastapi import FastAPI, HTTPException

from database import get_session, init_db
from models import Experiment


app = FastAPI(title="Eco Pack Analytics API", version="1.0.0")
init_db()


@app.get("/health")
def health():
    return {"status": "ok", "service": "eco-pack-analytics"}


@app.get("/experiments")
def experiments():
    session = get_session()
    try:
        return [
            {
                "id": item.id,
                "name": item.name,
                "date": item.experiment_date.isoformat(),
                "author": item.author,
                "samples": len(item.samples),
            }
            for item in session.query(Experiment).order_by(Experiment.id.desc()).all()
        ]
    finally:
        session.close()


@app.get("/experiments/{experiment_id}")
def experiment_detail(experiment_id: int):
    session = get_session()
    try:
        item = session.get(Experiment, experiment_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Эксперимент не найден")
        return {
            "id": item.id,
            "name": item.name,
            "date": item.experiment_date.isoformat(),
            "author": item.author,
            "description": item.description,
            "samples": [
                {
                    "id": sample.id,
                    "name": sample.name,
                    "composition": sample.composition,
                    "quality": {field: getattr(sample.quality, field) for field in ("flexibility", "strength", "water_resistance", "water_stability", "biodegradability")},
                    "mass": [{"day": measurement.day, "mass": measurement.mass} for measurement in sample.mass_measurements],
                }
                for sample in item.samples
            ],
        }
    finally:
        session.close()