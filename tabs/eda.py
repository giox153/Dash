"""
eda.py
Pestaña 2: Análisis Exploratorio de Datos (EDA).
Genera todas las figuras directamente desde los datos sintéticos.
"""

import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import html, dcc

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data.generate_data import generate_attrition_data

# ── Paleta pastel coherente ────────────────────────────────────
PASTEL = ["#A4C2F4", "#F28B82", "#A8D8A8", "#FBBC04", "#C5A3FF"]
COLOR_NO  = "#A4C2F4"   # azul pastel → se queda
COLOR_SI  = "#F28B82"   # rojo pastel → abandona


def _chart_card(titulo: str, figura_id: str, figura) -> dbc.Card:
    """Envuelve un gráfico Plotly en una card con título."""
    return dbc.Card([
        dbc.CardHeader(
            html.H6(titulo, className="mb-0 fw-semibold",
                    style={"color": "#444", "fontSize": "0.9rem"}),
            style={"backgroundColor": "#FAFAFA", "border": "none",
                   "paddingTop": "1rem", "paddingBottom": "0.5rem"},
        ),
        dbc.CardBody(
            dcc.Graph(id=figura_id, figure=figura,
                      config={"displayModeBar": False},
                      style={"height": "320px"}),
            style={"padding": "0.5rem 1rem 1rem"},
        ),
    ], style={"border": "none", "borderRadius": "16px",
              "boxShadow": "0 2px 12px rgba(0,0,0,0.07)"})


def _dona_abandono(df: pd.DataFrame) -> go.Figure:
    counts = df["abandono"].value_counts()
    fig = go.Figure(go.Pie(
        labels=["Se queda", "Abandona"],
        values=[counts.get(0, 0), counts.get(1, 0)],
        hole=0.55,
        marker_colors=[COLOR_NO, COLOR_SI],
        textinfo="label+percent",
        textfont_size=13,
    ))
    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(text="Abandono", x=0.5, y=0.5,
                          font_size=14, showarrow=False,
                          font_color="#555")],
    )
    return fig


def _bar_departamento(df: pd.DataFrame) -> go.Figure:
    agrup = (
        df.groupby(["departamento", "abandono"])
        .size().reset_index(name="conteo")
    )
    agrup["etiqueta"] = agrup["abandono"].map({0: "Se queda", 1: "Abandona"})
    fig = px.bar(
        agrup, x="departamento", y="conteo",
        color="etiqueta",
        color_discrete_map={"Se queda": COLOR_NO, "Abandona": COLOR_SI},
        barmode="group",
        labels={"conteo": "Empleados", "departamento": "",
                "etiqueta": "Estado"},
    )
    fig.update_layout(
        margin=dict(t=10, b=40, l=40, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(title="", orientation="h", y=1.08),
        yaxis=dict(gridcolor="#F0F0F0"),
        xaxis=dict(showgrid=False),
        font=dict(size=12),
    )
    return fig


def _hist_satisfaccion(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df, x="satisfaccion", color=df["abandono"].map({0: "Se queda", 1: "Abandona"}),
        color_discrete_map={"Se queda": COLOR_NO, "Abandona": COLOR_SI},
        barmode="overlay", opacity=0.78,
        labels={"satisfaccion": "Satisfacción (1–5)",
                "color": "Estado", "count": "Empleados"},
        nbins=5,
    )
    fig.update_layout(
        margin=dict(t=10, b=40, l=40, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(title=""),
        yaxis=dict(gridcolor="#F0F0F0"),
        xaxis=dict(showgrid=False),
    )
    return fig


def _hist_salario(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df, x="salario",
        color=df["abandono"].map({0: "Se queda", 1: "Abandona"}),
        color_discrete_map={"Se queda": COLOR_NO, "Abandona": COLOR_SI},
        barmode="overlay", opacity=0.78,
        labels={"salario": "Salario (COP)", "color": "Estado"},
        nbins=30,
    )
    fig.update_layout(
        margin=dict(t=10, b=40, l=40, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(title=""),
        yaxis=dict(gridcolor="#F0F0F0"),
        xaxis=dict(showgrid=False),
    )
    return fig


def _heatmap_correlacion(df: pd.DataFrame) -> go.Figure:
    cols_num = ["edad", "salario", "años_empresa", "satisfaccion",
                "horas_trabajadas", "promociones", "abandono"]
    corr = df[cols_num].corr().round(2)

    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.columns.tolist(),
        colorscale=[
            [0.0, "#F28B82"],
            [0.5, "#FFFFFF"],
            [1.0, "#A4C2F4"],
        ],
        zmin=-1, zmax=1,
        text=corr.values,
        texttemplate="%{text}",
        textfont={"size": 11},
        showscale=True,
    ))
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
    )
    return fig


def layout() -> html.Div:
    """Retorna el layout completo de la pestaña EDA."""
    df = generate_attrition_data()

    tasa_abandono = df["abandono"].mean() * 100
    total = len(df)
    abandonan = df["abandono"].sum()

    return html.Div([

        # ── Encabezado ─────────────────────────────────────────
        html.Span("ANÁLISIS EXPLORATORIO", className="eyebrow-label"),
        html.H2("Patrones en los datos", className="hero-title mt-2 mb-1"),
        html.P(f"Dataset: {total:,} empleados · Tasa de abandono: {tasa_abandono:.1f}%",
               className="text-muted mb-4", style={"fontSize": "0.9rem"}),

        # ── Fila 1: Dona + Barras ──────────────────────────────
        dbc.Row([
            dbc.Col(_chart_card(
                "Distribución general de abandono",
                "dona-abandono", _dona_abandono(df)
            ), xs=12, md=5, className="mb-4"),
            dbc.Col(_chart_card(
                "Abandono por departamento",
                "bar-depto", _bar_departamento(df)
            ), xs=12, md=7, className="mb-4"),
        ]),

        # ── Fila 2: Histogramas ────────────────────────────────
        dbc.Row([
            dbc.Col(_chart_card(
                "Distribución de satisfacción laboral",
                "hist-satisf", _hist_satisfaccion(df)
            ), xs=12, md=6, className="mb-4"),
            dbc.Col(_chart_card(
                "Distribución salarial",
                "hist-salario", _hist_salario(df)
            ), xs=12, md=6, className="mb-4"),
        ]),

        # ── Fila 3: Correlación ────────────────────────────────
        dbc.Row([
            dbc.Col(_chart_card(
                "Mapa de correlación entre variables",
                "heatmap-corr", _heatmap_correlacion(df)
            ), xs=12, className="mb-4"),
        ]),

    ], className="tab-content-wrapper")