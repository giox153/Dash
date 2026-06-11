"""
prediccionmodelo.py
Pestaña 4: Predicción interactiva de abandono laboral en tiempo real.
Carga model.pkl y expone un formulario para scoring individual.
"""

import sys
import os
import joblib
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback, no_update

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "model.pkl")
DEPARTAMENTOS = ["Ventas", "TI", "RRHH", "Finanzas", "Operaciones"]

COLOR_RIESGO_ALTO  = "#F28B82"
COLOR_RIESGO_BAJO  = "#A8D8A8"
COLOR_RIESGO_MEDIO = "#FBBC04"


def _label_input(label: str, componente) -> dbc.Row:
    """Fila de formulario: etiqueta arriba, componente abajo."""
    return dbc.Row([
        dbc.Col([
            html.Label(label, style={"fontSize": "0.82rem",
                                     "fontWeight": "600",
                                     "color": "#555",
                                     "marginBottom": "4px"}),
            componente,
        ]),
    ], className="mb-3")


def layout() -> html.Div:
    """Retorna el layout de la pestaña de predicción."""
    return html.Div([

        html.Span("PREDICCIÓN EN TIEMPO REAL", className="eyebrow-label"),
        html.H2("Perfil del empleado", className="hero-title mt-2 mb-1"),
        html.P("Completa los datos del empleado y obtén su probabilidad de abandono.",
               className="text-muted mb-4", style={"fontSize": "0.9rem"}),

        dbc.Row([

            # ── Formulario ─────────────────────────────────────
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([

                        dbc.Row([
                            dbc.Col(_label_input("Edad (años)", dcc.Slider(
                                id="inp-edad", min=22, max=60, step=1, value=32,
                                marks={22: "22", 40: "40", 60: "60"},
                                tooltip={"placement": "bottom", "always_visible": True},
                            )), md=6),
                            dbc.Col(_label_input("Años en la empresa", dcc.Slider(
                                id="inp-anios", min=0, max=20, step=1, value=3,
                                marks={0: "0", 10: "10", 20: "20"},
                                tooltip={"placement": "bottom", "always_visible": True},
                            )), md=6),
                        ]),

                        _label_input("Salario mensual (COP)", dcc.Slider(
                            id="inp-salario",
                            min=1_800_000, max=9_000_000, step=100_000,
                            value=3_500_000,
                            marks={
                                1_800_000: "$1.8M",
                                4_500_000: "$4.5M",
                                9_000_000: "$9M",
                            },
                            tooltip={"placement": "bottom", "always_visible": True},
                        )),

                        dbc.Row([
                            dbc.Col(_label_input("Satisfacción laboral (1–5)",
                                dcc.Slider(
                                    id="inp-satisf", min=1, max=5, step=1, value=3,
                                    marks={1: "1 😞", 3: "3 😐", 5: "5 😊"},
                                    tooltip={"placement": "bottom", "always_visible": True},
                                )
                            ), md=6),
                            dbc.Col(_label_input("Horas trabajadas / semana",
                                dcc.Slider(
                                    id="inp-horas", min=35, max=65, step=1, value=45,
                                    marks={35: "35h", 50: "50h", 65: "65h"},
                                    tooltip={"placement": "bottom", "always_visible": True},
                                )
                            ), md=6),
                        ]),

                        dbc.Row([
                            dbc.Col(_label_input("Promociones recibidas",
                                dcc.Slider(
                                    id="inp-promociones", min=0, max=5, step=1, value=1,
                                    marks={i: str(i) for i in range(6)},
                                    tooltip={"placement": "bottom", "always_visible": True},
                                )
                            ), md=6),
                            dbc.Col(_label_input("Departamento",
                                dbc.Select(
                                    id="inp-depto",
                                    options=[{"label": d, "value": d} for d in DEPARTAMENTOS],
                                    value="TI",
                                    style={"borderRadius": "10px", "fontSize": "0.9rem"},
                                )
                            ), md=6),
                        ]),

                        # Botón
                        dbc.Button(
                            "Calcular riesgo de abandono →",
                            id="btn-predecir",
                            color="primary",
                            className="mt-2 w-100",
                            style={"borderRadius": "10px",
                                   "fontWeight": "600",
                                   "backgroundColor": "#A4C2F4",
                                   "border": "none",
                                   "color": "#333"},
                        ),

                    ], className="p-4"),
                ], style={"border": "none", "borderRadius": "16px",
                          "boxShadow": "0 2px 12px rgba(0,0,0,0.07)"}),
            ], xs=12, lg=7, className="mb-4"),

            # ── Panel de resultado ─────────────────────────────
            dbc.Col([
                html.Div(id="panel-resultado", children=[
                    dbc.Card([
                        dbc.CardBody([
                            html.Div("⬅️", style={"fontSize": "2.5rem"}),
                            html.H6("Completa el formulario",
                                    className="fw-semibold mt-3 mb-1",
                                    style={"color": "#555"}),
                            html.P("El resultado aparecerá aquí.",
                                   className="text-muted",
                                   style={"fontSize": "0.85rem"}),
                        ], className="text-center py-5"),
                    ], style={"border": "none", "borderRadius": "16px",
                              "backgroundColor": "#F9F9FF",
                              "boxShadow": "0 2px 10px rgba(0,0,0,0.05)",
                              "minHeight": "380px"}),
                ]),
            ], xs=12, lg=5, className="mb-4"),

        ]),

    ], className="tab-content-wrapper")


# ── Callback de predicción ─────────────────────────────────────
@callback(
    Output("panel-resultado", "children"),
    Input("btn-predecir", "n_clicks"),
    State("inp-edad",       "value"),
    State("inp-salario",    "value"),
    State("inp-anios",      "value"),
    State("inp-satisf",     "value"),
    State("inp-horas",      "value"),
    State("inp-promociones","value"),
    State("inp-depto",      "value"),
    prevent_initial_call=True,
)
def predecir(n_clicks, edad, salario, anios, satisf, horas, promos, depto):
    """Carga el modelo pkl y devuelve la probabilidad de abandono."""
    if not n_clicks:
        return no_update

    pipeline = joblib.load(MODEL_PATH)

    entrada = pd.DataFrame([{
        "edad":            edad,
        "salario":         salario,
        "años_empresa":    anios,
        "satisfaccion":    satisf,
        "horas_trabajadas":horas,
        "promociones":     promos,
        "departamento":    depto,
    }])

    proba = pipeline.predict_proba(entrada)[0][1]
    pred  = pipeline.predict(entrada)[0]

    # Clasificación de riesgo
    if proba < 0.35:
        nivel, color, emoji = "Riesgo Bajo", COLOR_RIESGO_BAJO, "🟢"
    elif proba < 0.60:
        nivel, color, emoji = "Riesgo Medio", COLOR_RIESGO_MEDIO, "🟡"
    else:
        nivel, color, emoji = "Riesgo Alto", COLOR_RIESGO_ALTO, "🔴"

    # Factores destacados
    factores = []
    if satisf <= 2:
        factores.append("Satisfacción laboral muy baja")
    if salario < 3_000_000:
        factores.append("Salario por debajo del promedio")
    if horas > 55:
        factores.append("Sobrecarga laboral (>55 h/sem)")
    if anios < 2:
        factores.append("Poco tiempo en la empresa")
    if promos == 0:
        factores.append("Sin promociones registradas")
    if not factores:
        factores.append("Sin factores de riesgo críticos detectados")

    return dbc.Card([
        dbc.CardBody([
            html.Div(emoji, style={"fontSize": "3rem"}),
            html.H2(f"{proba:.1%}", className="fw-bold mt-2 mb-0",
                    style={"fontSize": "3rem", "color": "#333"}),
            html.P("Probabilidad de abandono",
                   className="text-muted mb-3",
                   style={"fontSize": "0.85rem"}),

            dbc.Badge(nivel, style={
                "backgroundColor": color,
                "color": "#333",
                "fontSize": "0.85rem",
                "padding": "6px 16px",
                "borderRadius": "20px",
                "fontWeight": "600",
            }),

            html.Hr(style={"margin": "1.2rem 0"}),

            html.H6("Factores detectados", className="fw-semibold mb-2",
                    style={"fontSize": "0.85rem", "color": "#555",
                           "textAlign": "left"}),
            html.Ul([
                html.Li(f, style={"fontSize": "0.82rem",
                                  "color": "#666",
                                  "marginBottom": "4px"})
                for f in factores
            ], style={"paddingLeft": "1.2rem", "textAlign": "left"}),

        ], className="text-center p-4"),
    ], style={
        "border": "none",
        "borderRadius": "16px",
        "backgroundColor": f"{color}22",
        "boxShadow": f"0 4px 20px {color}44",
        "minHeight": "380px",
    })