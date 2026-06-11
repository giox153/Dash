"""
train_model.py
Entrena una regresión logística para predecir abandono laboral
y serializa el pipeline completo en model.pkl.
"""

import sys
import os
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report

# Asegurar que el path raíz esté disponible
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.generate_data import generate_attrition_data

# ── Configuración ──────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

FEATURES_NUM = ["edad", "salario", "años_empresa", "satisfaccion",
                "horas_trabajadas", "promociones"]
FEATURES_CAT = ["departamento"]
TARGET = "abandono"


def build_pipeline() -> Pipeline:
    """Construye el pipeline de preprocesamiento + clasificador."""
    preprocessor = ColumnTransformer(transformers=[
        ("num", StandardScaler(), FEATURES_NUM),
        ("cat", OneHotEncoder(handle_unknown="ignore"), FEATURES_CAT),
    ])

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(
            max_iter=500,
            class_weight="balanced",
            random_state=42,
        )),
    ])
    return pipeline


def train_and_save():
    """Genera datos, entrena el modelo y lo guarda en disco."""
    print("📊 Generando datos sintéticos...")
    df = generate_attrition_data(n=1000)

    X = df[FEATURES_NUM + FEATURES_CAT]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("🔧 Entrenando pipeline de regresión logística...")
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    # Reporte en consola
    y_pred = pipeline.predict(X_test)
    print("\n📋 Reporte de clasificación (test set):")
    print(classification_report(y_test, y_pred, target_names=["Se queda", "Abandona"]))

    # Persistencia
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\n✅ Modelo guardado en: {MODEL_PATH}")

    # Devolver también los splits para uso externo
    return pipeline, X_test, y_test


if __name__ == "__main__":
    train_and_save()