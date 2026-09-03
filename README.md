# Eco Pack Analytics

Модульная система для цифрового анализа биопластика: SQLite + SQLAlchemy, Streamlit multi-page, pandas/numpy/scikit-learn и Plotly.

## Запуск

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

REST API запускается отдельно командой `uvicorn api:app --reload --port 8000`.

При первом открытии создается `ecopack.db` с демонстрационным экспериментом на четырех образцах. Реальные данные загружаются на странице «Управление экспериментами» в XLSX/CSV.

## Формат импорта

Обязательные поля: `experiment`, `sample`, `composition`, `flexibility`, `strength`, `water_resistance`, `water_stability`, `biodegradability`, `mass_1`, `mass_3`, `mass_5`, `mass_7`, `mass_10`, `mass_14`.

Критерии и масса должны быть неотрицательными и числовыми. Аналитика нормализует критерии MinMaxScaler, считает взвешенную MCDA-оценку и строит квадратичный прогноз массы до 60-го дня. Отчеты доступны в Excel и PDF.
