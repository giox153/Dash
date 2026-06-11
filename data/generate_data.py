"""
generate_data.py
Genera dataset sintético de rotación laboral (employee attrition).
"""

import numpy as np
import pandas as pd

def generate_attrition_data(n: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Genera un DataFrame sintético con variables relevantes para
    predicción de rotación laboral.

    Args:
        n: Número de registros.
        seed: Semilla para reproducibilidad.

    Returns:
        pd.DataFrame con columnas de empleados y etiqueta 'abandono'.
    """
    rng = np.random.default_rng(seed)

    departamentos = ["Ventas", "TI", "RRHH", "Finanzas", "Operaciones"]
    departamento = rng.choice(departamentos, size=n, p=[0.30, 0.25, 0.15, 0.15, 0.15])

    edad = rng.integers(22, 60, size=n)
    años_empresa = np.clip(rng.integers(0, 20, size=n), 0, edad - 22)
    salario = rng.integers(1_800_000, 9_000_000, size=n)
    satisfaccion = rng.integers(1, 6, size=n)          # 1 = muy insatisfecho, 5 = muy satisfecho
    horas_trabajadas = rng.integers(35, 65, size=n)
    promociones = rng.integers(0, 5, size=n)

    # Lógica de abandono ponderada por factores de riesgo reales
    riesgo = (
        (satisfaccion < 3).astype(float) * 0.35
        + (salario < 3_000_000).astype(float) * 0.20
        + (horas_trabajadas > 55).astype(float) * 0.15
        + (años_empresa < 2).astype(float) * 0.15
        + (promociones == 0).astype(float) * 0.10
        + rng.uniform(0, 0.15, size=n)                 # ruido aleatorio
    )
    abandono = (riesgo > 0.45).astype(int)

    df = pd.DataFrame({
        "edad": edad,
        "salario": salario,
        "años_empresa": años_empresa,
        "departamento": departamento,
        "satisfaccion": satisfaccion,
        "horas_trabajadas": horas_trabajadas,
        "promociones": promociones,
        "abandono": abandono,
    })

    return df


if __name__ == "__main__":
    df = generate_attrition_data()
    print(df.head())
    print(f"\nDistribución abandono:\n{df['abandono'].value_counts(normalize=True).round(3)}")