"""
contextoproblema.py
Pestaña 1: Contexto del problema de rotación laboral.
Layout completamente desacoplado del resto de la app.
"""

import dash_bootstrap_components as dbc
from dash import html


# ── Paleta pastel (consistente con style.css) ──────────────────
COLOR_RIESGO   = "#F28B82"   # rojo pastel
COLOR_COSTO    = "#FBBC04"   # amarillo pastel
COLOR_MODELO   = "#A8D8A8"   # verde pastel
COLOR_ACCION   = "#A4C2F4"   # azul pastel


def _stat_card(valor: str, etiqueta: str, color: str) -> dbc.Col:
    """Tarjeta de KPI rápida para la sección de impacto."""
    return dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.H2(valor, className="fw-bold mb-1",
                        style={"color": "#3d3d3d", "fontSize": "2rem"}),
                html.P(etiqueta, className="text-muted mb-0",
                       style={"fontSize": "0.85rem"}),
            ], className="text-center py-4"),
        ], style={"backgroundColor": color, "border": "none",
                  "borderRadius": "16px", "boxShadow": "0 2px 12px rgba(0,0,0,0.07)"}),
        xs=12, sm=6, lg=3, className="mb-3",
    )


def _factor_card(icono: str, titulo: str, descripcion: str) -> dbc.Col:
    """Tarjeta de factor de riesgo."""
    return dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.Div(icono, style={"fontSize": "2rem", "marginBottom": "0.5rem"}),
                html.H6(titulo, className="fw-semibold mb-2",
                        style={"color": "#444"}),
                html.P(descripcion, className="text-muted mb-0",
                       style={"fontSize": "0.82rem", "lineHeight": "1.5"}),
            ], className="text-center p-4"),
        ], style={"border": "none", "borderRadius": "16px",
                  "backgroundColor": "#F9F9FF",
                  "boxShadow": "0 2px 10px rgba(0,0,0,0.06)"}),
        xs=12, sm=6, lg=3, className="mb-3",
    )


def layout() -> html.Div:
    """
    Retorna el layout completo de la pestaña Contexto del Problema.
    """
    return html.Div([

        # ── Hero ────────────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                html.Span("ROTACIÓN LABORAL", className="eyebrow-label"),
                html.H1("¿Por qué un empleado decide irse?",
                        className="hero-title mt-2 mb-3"),
                html.P(
                    "La rotación no planificada es uno de los mayores costos ocultos "
                    "de las organizaciones. Anticiparla con datos permite actuar antes "
                    "de que el talento abandone la empresa.",
                    style={"fontSize": "1.05rem", "color": "#555",
                           "maxWidth": "620px", "lineHeight": "1.7"},
                ),
            ], lg=8, className="mb-4"),
        ]),

        html.Hr(className="section-divider"),

        # ── KPIs de impacto ────────────────────────────────────
        html.H5("Impacto empresarial medible",
                className="section-title mb-4"),
        dbc.Row([
            _stat_card("~21%",  "Salario anual que cuesta reemplazar un empleado",  COLOR_RIESGO),
            _stat_card("3–6 m", "Tiempo promedio para cubrir una vacante crítica",   COLOR_COSTO),
            _stat_card("34%",   "De rotación es atribuible a insatisfacción evitable", COLOR_MODELO),
            _stat_card("2×",    "Mayor retención con programas de predicción temprana", COLOR_ACCION),
        ], className="mb-5"),

        html.Hr(className="section-divider"),

        # ── Factores de riesgo ─────────────────────────────────
        html.H5("Factores clave de riesgo",
                className="section-title mb-4"),
        dbc.Row([
            _factor_card("😞", "Baja satisfacción",
                         "Empleados con puntuación ≤ 2 tienen 3× más probabilidad de abandonar."),
            _factor_card("💰", "Salario por debajo del mercado",
                         "La brecha salarial es el detonante #1 de búsqueda activa de empleo."),
            _factor_card("⏰", "Sobrecarga laboral",
                         "Más de 55 h/semana sostenidas elevan el riesgo de burnout y renuncia."),
            _factor_card("📈", "Falta de promociones",
                         "Sin crecimiento visible en 2+ años, el compromiso cae significativamente."),
        ], className="mb-5"),

        html.Hr(className="section-divider"),

        # ── Objetivo del proyecto ──────────────────────────────
        html.H5("Objetivo de este dashboard", className="section-title mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(html.Div("🎯", style={"fontSize": "2.5rem"}), width="auto"),
                            dbc.Col([
                                html.H6("Predicción individual en tiempo real",
                                        className="fw-semibold mb-1"),
                                html.P("Ingresa el perfil de cualquier empleado y obtén "
                                       "la probabilidad estimada de que abandone la organización, "
                                       "junto con los factores que más influyen en esa decisión.",
                                       className="text-muted mb-0",
                                       style={"fontSize": "0.9rem"}),
                            ]),
                        ], align="center"),
                    ]),
                ], style={"border": "none", "borderRadius": "16px",
                          "backgroundColor": "#EEF4FF",
                          "boxShadow": "0 2px 10px rgba(0,0,0,0.06)"}),
            ], lg=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(html.Div("📊", style={"fontSize": "2.5rem"}), width="auto"),
                            dbc.Col([
                                html.H6("Exploración de patrones organizacionales",
                                        className="fw-semibold mb-1"),
                                html.P("Visualiza cómo se distribuye la rotación por departamento, "
                                       "edad, salario y satisfacción, para identificar poblaciones "
                                       "de alto riesgo de forma agregada.",
                                       className="text-muted mb-0",
                                       style={"fontSize": "0.9rem"}),
                            ]),
                        ], align="center"),
                    ]),
                ], style={"border": "none", "borderRadius": "16px",
                          "backgroundColor": "#F0FFF4",
                          "boxShadow": "0 2px 10px rgba(0,0,0,0.06)"}),
            ], lg=6),
        ]),

    ], className="tab-content-wrapper")