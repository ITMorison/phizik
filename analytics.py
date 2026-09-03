from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

CRITERIA = {
    "Иілгіштік": "flexibility",
    "Беріктік": "strength",
    "Суға төзімділік": "water_resistance",
    "Суда тұрақтылық": "water_stability",
    "Биоыдырау": "biodegradability",
}
DAYS = [1, 3, 5, 7, 10, 14]
DEFAULT_WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.20]


def normalize_and_score(criteria: pd.DataFrame, weights: list[float]) -> pd.DataFrame:
    if criteria.empty:
        return pd.DataFrame()
    scaler = MinMaxScaler()
    values = criteria[list(CRITERIA)].astype(float)
    normalized = pd.DataFrame(scaler.fit_transform(values), columns=list(CRITERIA), index=criteria.index)
    normalized["Жалпы баға"] = normalized[list(CRITERIA)].mul(weights).sum(axis=1)
    return normalized


def forecast_mass(days: list[int], masses: list[float], horizon: int = 60) -> pd.DataFrame:
    clean = pd.DataFrame({"day": days, "mass": masses}).dropna()
    if len(clean) < 2:
        return pd.DataFrame({"day": days, "mass": masses, "kind": "Факт"})
    degree = min(2, len(clean) - 1)
    coefficients = np.polyfit(clean["day"], clean["mass"], degree)
    future_days = np.arange(int(clean.day.max()) + 1, horizon + 1)
    future_mass = np.maximum(0, np.polyval(coefficients, future_days))
    actual = pd.DataFrame({"day": clean.day, "mass": clean.mass, "kind": "Факт"})
    forecast = pd.DataFrame({"day": future_days, "mass": future_mass, "kind": "Прогноз"})
    return pd.concat([actual, forecast], ignore_index=True)


def recommendation(scores: pd.DataFrame, compositions: dict[str, str]) -> tuple[str, float, str]:
    if scores.empty:
        return "Нет данных", 0.0, "Добавьте образцы для формирования рекомендации."
    winner = scores["Жалпы баға"].idxmax()
    score = float(scores.loc[winner, "Жалпы баға"])
    composition = compositions.get(winner, "состав не указан")
    return winner, score, f"{winner} лидирует по сбалансированной MCDA-оценке ({score:.2f}/1.00). Состав: {composition}."
