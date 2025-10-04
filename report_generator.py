# report_generator.py

import pandas as pd
from io import BytesIO
from fpdf import FPDF

def convertir_df_a_excel(df):
    """Convierte un DataFrame a un archivo Excel en memoria."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Reporte')
    processed_data = output.getvalue()
    return processed_data

def convertir_df_a_pdf(df, titulo="Reporte"):
    """Convierte un DataFrame a un archivo PDF en memoria."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, titulo, 0, 1, 'C')
    pdf.ln(10)

    pdf.set_font("Arial", "B", 10)
    columnas = df.columns
    ancho_pagina = 190
    try:
        ancho_col = ancho_pagina / len(columnas)
    except ZeroDivisionError:
        ancho_col = ancho_pagina
        
    for col in columnas:
        pdf.cell(ancho_col, 10, col, 1, 0, 'C')
    pdf.ln()

    pdf.set_font("Arial", "", 10)
    for index, row in df.iterrows():
        for col in columnas:
            pdf.cell(ancho_col, 10, str(row[col]), 1, 0, 'L')
        pdf.ln()
    
    # --- CAMBIO DEFINITIVO AQUÍ ---
    # Convertimos el resultado de FPDF (que es bytearray) al tipo 'bytes' que Streamlit espera.
    return bytes(pdf.output())

def convertir_df_a_csv(df):
    """Convierte un DataFrame a un objeto CSV en memoria."""
    return df.to_csv(index=False).encode('utf-8')