"""
app.py
Punto de entrada principal del dashboard de rotación laboral.
Importa el layout de cada pestaña desde /tabs.
"""

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output

# Importar layouts de cada pestaña
from tabs.contextoproblema import layout as layout_contexto
from tabs.eda               import layout as layout_eda
from tabs.metricasmodelo    import layout as layout_metricas
from tabs.prediccionmodelo  import layout as layout_prediccion

# ── Inicialización ─────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="Rotación Laboral · Analytics",
)
server = app.server   # para despliegue con gunicorn si se requiere


# ── Layout principal ───────────────────────────────────────────
app.layout = dbc.Container([

    # Barra superior
    dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row([
                    dbc.Col(html.Span("👥", style={"fontSize": "1.3rem"})),
                    dbc.Col(dbc.NavbarBrand("AttritionIQ", className="ms-1")),
                ], align="center"),
                href="#", style={"textDecoration": "none"},
            ),
            html.Span("Employee Attrition Analytics · v1.0",
                      style={"fontSize": "0.78rem", "color": "#999",
                             "marginLeft": "1rem"}),
        ], fluid=True),
        color="white",
        style={"boxShadow": "0 1px 8px rgba(0,0,0,0.07)",
               "marginBottom": "0"},
    ),

    # Tabs de navegación
    dbc.Tabs(
        id="tabs-principal",
        active_tab="tab-contexto",
        children=[
            dbc.Tab(label="📋 Contexto",      tab_id="tab-contexto"),
            dbc.Tab(label="🔍 EDA",           tab_id="tab-eda"),
            dbc.Tab(label="📊 Métricas",      tab_id="tab-metricas"),
            dbc.Tab(label="🤖 Predicción",    tab_id="tab-prediccion"),
        ],
        style={"backgroundColor": "white",
               "paddingLeft": "1rem",
               "paddingTop": "0.5rem",
               "borderBottom": "none"},
    ),

    # Contenedor dinámico de contenido
    html.Div(id="contenido-tab"),

], fluid=True, style={"padding": "0", "maxWidth": "1280px"})


# ── Callback de navegación ─────────────────────────────────────
@app.callback(
    Output("contenido-tab", "children"),
    Input("tabs-principal", "active_tab"),
)
def render_tab(tab: str) -> html.Div:
    """Renderiza el layout correspondiente según la pestaña activa."""
    if tab == "tab-contexto":
        return layout_contexto()
    elif tab == "tab-eda":
        return layout_eda()
    elif tab == "tab-metricas":
        return layout_metricas()
    elif tab == "tab-prediccion":
        return layout_prediccion()
    return html.Div("Pestaña no encontrada.", className="p-4 text-muted")


# ── Punto de entrada ───────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=8050)