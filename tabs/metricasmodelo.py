"""
metricasmodelo.py
Pestaña 3: Métricas de evaluación del modelo de regresión logística.
"""

import sys
import os
import joblib
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import html, dcc
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, auc,
)
from sklearn.model_selection import train_test_split

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.generate_data import generate_attrition_data

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "model.pkl")
FEATURES   = ["edad", "salario", "años_empresa", "satisfaccion",
               "horas_trabajadas", "promociones", "departamento"]
TARGET     = "abandono"

COLOR_NO = "#A4C2F4"
COLOR_SI = "#F28B82"


def _cargar_resultados():
    """Carga modelo y genera predicciones sobre el conjunto de test."""
    pipeline = joblib.load(MODEL_PATH)
    df = generate_attrition_data()
    X = df[FEATURES]
    y = df[TARGET]
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    y_pred  = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    return y_test, y_pred, y_proba


def _kpi_card(valor: str, etiqueta: str, color: str, icono: str) -> dbc.Col:
    return dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Div(icono, style={"fontSize": "1.5rem"}),
                html.H3(valor, className="fw-bold mb-0 mt-1",
                        style={"color": "#333", "fontSize": "1.8rem"}),
                html.P(etiqueta, className="text-muted mb-0",
                       style={"fontSize": "0.78rem"}),
            ], className="text-center py-3"),
        ], style={"backgroundColor": color, "border": "none",
                  "borderRadius": "16px",
                  "boxShadow": "0 2px 10px rgba(0,0,0,0.07)"}),
        xs=6, lg=3, className="mb-3",
    )


def _fig_roc(y_test, y_proba) -> go.Figure:
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode="lines",
        name=f"ROC (AUC = {roc_auc:.3f})",
        line=dict(color="#A4C2F4", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(164,194,244,0.15)",
    ))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode="lines",
        name="Clasificador aleatorio",
        line=dict(color="#CCC", dash="dash", width=1.5),
    ))
    fig.update_layout(
        xaxis_title="Tasa de Falsos Positivos",
        yaxis_title="Tasa de Verdaderos Positivos",
        margin=dict(t=20, b=50, l=50, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.25),
        yaxis=dict(gridcolor="#F0F0F0"),
        xaxis=dict(gridcolor="#F0F0F0"),
        font=dict(size=12),
    )
    return fig


def _fig_confusion(y_test, y_pred) -> go.Figure:
    cm = confusion_matrix(y_test, y_pred)
    etiquetas = ["Se queda", "Abandona"]

    fig = go.Figure(go.Heatmap(
        z=cm,
        x=etiquetas,
        y=etiquetas,
        colorscale=[
            [0.0, "#FFFFFF"],
            [1.0, "#A4C2F4"],
        ],
        showscale=False,
        text=cm,
        texttemplate="<b>%{text}</b>",
        textfont={"size": 18},
    ))
    fig.update_layout(
        xaxis_title="Predicción",
        yaxis_title="Real",
        margin=dict(t=20, b=50, l=60, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=12),
    )
    return fig


def layout() -> html.Div:
    """Retorna el layout de la pestaña Métricas del Modelo."""
    y_test, y_pred, y_proba = _cargar_resultados()

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec  = recall_score(y_test, y_pred)
    f1   = f1_score(y_test, y_pred)

    return html.Div([

        html.Span("EVALUACIÓN DEL MODELO", className="eyebrow-label"),
        html.H2("Métricas de desempeño", className="hero-title mt-2 mb-1"),
        html.P("Regresión logística · Conjunto de prueba (20% de los datos)",
               className="text-muted mb-4", style={"fontSize": "0.9rem"}),

        # ── KPIs ───────────────────────────────────────────────
        dbc.Row([
            _kpi_card(f"{acc:.1%}",  "Accuracy",   "#EEF4FF", "🎯"),
            _kpi_card(f"{prec:.1%}", "Precision",  "#FFF4E5", "🔍"),
            _kpi_card(f"{rec:.1%}",  "Recall",     "#F0FFF4", "📡"),
            _kpi_card(f"{f1:.1%}",   "F1-Score",   "#FFF0F3", "⚖️"),
        ], className="mb-5"),

        html.Hr(className="section-divider"),
        html.H5("Visualizaciones de evaluación",
                className="section-title mb-4"),

        # ── ROC + Confusion ────────────────────────────────────
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.H6("Curva ROC", className="mb-0 fw-semibold",
                                style={"color": "#444", "fontSize": "0.9rem"}),
                        style={"backgroundColor": "#FAFAFA", "border": "none",
                               "paddingTop": "1rem"},
                    ),
                    dbc.CardBody(
                        dcc.Graph(id="roc-curve", figure=_fig_roc(y_test, y_proba),
                                  config={"displayModeBar": False},
                                  style={"height": "340px"}),
                        style={"padding": "0.5rem 1rem 1rem"},
                    ),
                ], style={"border": "none", "borderRadius": "16px",
                          "boxShadow": "0 2px 12px rgba(0,0,0,0.07)"}),
            ], xs=12, md=7, className="mb-4"),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.H6("Matriz de Confusión", className="mb-0 fw-semibold",
                                style={"color": "#444", "fontSize": "0.9rem"}),
                        style={"backgroundColor": "#FAFAFA", "border": "none",
                               "paddingTop": "1rem"},
                    ),
                    dbc.CardBody(
                        dcc.Graph(id="confusion-matrix", figure=_fig_confusion(y_test, y_pred),
                                  config={"displayModeBar": False},
                                  style={"height": "340px"}),
                        style={"padding": "0.5rem 1rem 1rem"},
                    ),
                ], style={"border": "none", "borderRadius": "16px",
                          "boxShadow": "0 2px 12px rgba(0,0,0,0.07)"}),
            ], xs=12, md=5, className="mb-4"),
        ]),

        # ── Interpretación ─────────────────────────────────────
        html.Hr(className="section-divider"),
        html.H5("Interpretación de resultados", className="section-title mb-3"),
        dbc.Row([
            dbc.Col(dbc.Alert([
                html.Strong("Precision: "),
                "De cada empleado marcado como 'en riesgo', ¿cuántos realmente abandonan? "
                "Alta precision → menos falsas alarmas para RRHH.",
            ], color="light", style={"borderLeft": f"4px solid {COLOR_NO}",
                                     "borderRadius": "12px"}), md=6, className="mb-3"),
            dbc.Col(dbc.Alert([
                html.Strong("Recall: "),
                "De todos los que realmente van a irse, ¿cuántos detectamos? "
                "Alto recall → no dejamos escapar casos críticos.",
            ], color="light", style={"borderLeft": f"4px solid {COLOR_SI}",
                                     "borderRadius": "12px"}), md=6, className="mb-3"),
        ]),

    ], className="tab-content-wrapper")