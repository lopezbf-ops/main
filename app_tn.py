import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

st.set_page_config(page_title="Calculadora TN Avanzada", layout="wide")

st.title("Calculadora de Patrones TN (Molde y Producción)")

# --- INTERFAZ DE ENTRADA ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**1. Inserto y Ajustes**")
    insert_w = st.number_input("Ancho del Inserto (cm)", value=10.5, step=0.1)
    insert_h = st.number_input("Alto del Inserto (cm)", value=14.8, step=0.1)
    spine_w = st.number_input("Ancho del Lomo (cm)", value=1.5, step=0.1)

with col2:
    st.markdown("**2. Holguras**")
    margin_x = st.number_input("Margen Lateral (cm)", value=0.5, step=0.1)
    margin_y = st.number_input("Margen Superior/Inferior (cm)", value=0.6, step=0.1)

with col3:
    st.markdown("**3. Solapa Interior (Izquierda)**")
    incluir_solapa = st.checkbox("Incluir solapa y costura", value=True)
    flap_w = st.number_input("Ancho de la solapa (cm)", value=8.5, step=0.1) if incluir_solapa else 0

st.divider()

# --- CÁLCULOS MATEMÁTICOS ---
# Cálculo exacto conservando 1 decimal (sin redondeo agresivo)
total_w = round(margin_x + insert_w + spine_w + insert_w + margin_x, 1)
total_h = round(margin_y + insert_h + margin_y, 1)

st.success(f"**PIEZA PRINCIPAL:** Cortar cuero a {total_w} cm de ancho x {total_h} cm de alto")
if incluir_solapa:
    st.info(f"**SOLAPA INTERIOR:** Cortar cuero a {flap_w} cm de ancho x {total_h} cm de alto")

# --- GENERADOR DEL PATRÓN PDF ---
def generar_grafico(escala_pdf=False):
    espacio_entre_piezas = 2 if incluir_solapa else 0
    fig_w = total_w + espacio_entre_piezas + flap_w if incluir_solapa else total_w
    fig_h = total_h
    
    dpi = 300 if escala_pdf else 100
    fig, ax = plt.subplots(figsize=(fig_w / 2.54, fig_h / 2.54), dpi=dpi)
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis('off')
    
    if escala_pdf:
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)

    # 1. PIEZA PRINCIPAL
    ax.add_patch(patches.Rectangle((0, 0), total_w, total_h, linewidth=1, edgecolor='black', facecolor='none'))
    center_x, center_y = total_w / 2, total_h / 2
    
    # Hoyos para elástico
    y_holes = [center_y, total_h - 1.0, total_h - 1.8, 1.0, 1.8]
    for y in y_holes:
        ax.add_patch(patches.Circle((center_x, y), 0.125, color='black'))

    # 2. SOLAPA Y COSTURA
    if incluir_solapa:
        stitch_r, margen_c, sep_c = 0.06, 0.4, 0.4
        y_costura = np.arange(margen_c, total_h, sep_c)
        x_costura_horiz = np.arange(margen_c + sep_c, flap_w, sep_c)

        # Costura Cuero Principal
        for y in y_costura: ax.add_patch(patches.Circle((margen_c, y), stitch_r, color='black'))
        for x in x_costura_horiz:
            ax.add_patch(patches.Circle((x, total_h - margen_c), stitch_r, color='black'))
            ax.add_patch(patches.Circle((x, margen_c), stitch_r, color='black'))

        # Solapa
        offset_x = total_w + espacio_entre_piezas
        ax.add_patch(patches.Rectangle((offset_x, 0), flap_w, total_h, linewidth=1, edgecolor='black', facecolor='none'))

        # Costura Solapa
        for y in y_costura: ax.add_patch(patches.Circle((offset_x + margen_c, y), stitch_r, color='black'))
        for x in x_costura_horiz:
            ax.add_patch(patches.Circle((offset_x + x, total_h - margen_c), stitch_r, color='black'))
            ax.add_patch(patches.Circle((offset_x + x, margen_c), stitch_r, color='black'))

    return fig

# --- GENERADOR DEL EXCEL ---
def generar_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Calculo_Corte_TN"

    dark_blue_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    light_blue_fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
    white_font, bold_font = Font(color="FFFFFF", bold=True), Font(bold=True)
    b_style = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    c_align, l_align = Alignment(horizontal='center', vertical='center'), Alignment(horizontal='left', vertical='center')

    ws.merge_cells('B2:E2')
    ws['B2'].value, ws['B2'].font, ws['B2'].alignment = "CALCULADORA DE MEDIDAS - TRAVELER'S NOTEBOOK (TONAL)", Font(size=14, bold=True, color="1F497D"), c_align
    
    headers = ["Parámetro", "Valor (cm)", "Descripción"]
    for col_num, header in enumerate(headers, start=2):
        cell = ws.cell(row=4, column=col_num, value=header)
        cell.fill, cell.font, cell.alignment, cell.border = dark_blue_fill, white_font, c_align, b_style

    data = [
        ("Ancho del Inserto", insert_w, "Ancho del cuadernillo cerrado"),
        ("Alto del Inserto", insert_h, "Alto del cuadernillo cerrado"),
        ("Ancho del Lomo", spine_w, "Espacio central para elásticos/cuadernillos"),
        ("Margen Lateral", margin_x, "Holgura izquierda y derecha"),
        ("Margen Superior/Inferior", margin_y, "Holgura arriba y abajo"),
        ("Ancho Solapa", flap_w, "Ancho de la solapa interior izquierda")
    ]

    for row_num, row_data in enumerate(data, start=5):
        for col_num, value in enumerate(row_data, start=2):
            cell = ws.cell(row=row_num, column=col_num, value=value)
            cell.border, cell.alignment = b_style, (c_align if col_num == 3 else l_align)
            if row_num % 2 == 0: cell.fill = light_blue_fill

    ws.merge_cells('B12:E12')
    ws['B12'].value, ws['B12'].font, ws['B12'].fill, ws['B12'].alignment = "CÁLCULO DE CORTE FINAL", Font(size=12, bold=True, color="FFFFFF"), dark_blue_fill, c_align

    formulas = [
        ("Ancho Bruto", "=C5+C5+C7+C8+C8", "Inserto + Inserto + Lomo + Margen(x2)"),
        ("Alto Bruto", "=C6+C9+C9", "Inserto + Margen Sup/Inf(x2)"),
        ("ANCHO DE CORTE FINAL", "=C13", "Medida exacta al decimal"),
        ("ALTO DE CORTE FINAL", "=C14", "Medida exacta al decimal"),
        ("SOLAPA INTERIOR (Ancho x Alto)", '=C10 & " x " & C16', "Ancho de solapa x Alto de corte")
    ]

    for row_num, row_data in enumerate(formulas, start=13):
        for col_num, value in enumerate(row_data, start=2):
            cell = ws.cell(row=row_num, column=col_num, value=value)
            cell.border, cell.alignment = b_style, (c_align if col_num == 3 else l_align)
            if col_num == 3: cell.font = bold_font
            if row_num in [15, 16, 17] and col_num == 3:
                cell.fill, cell.font = PatternFill(start_color="E2EFDA", fill_type="solid"), Font(bold=True, color="375623")

    ws.column_dimensions['B'].width, ws.column_dimensions['C'].width, ws.column_dimensions['D'].width = 30, 15, 45
    
    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)
    return excel_buffer

# --- VISUALIZACIÓN Y DESCARGAS ---
st.markdown("**Vista Previa del Patrón**")
fig_visual = generar_grafico(escala_pdf=False)
st.pyplot(fig_visual)

fig_pdf = generar_grafico(escala_pdf=True)
pdf_buffer = io.BytesIO()
fig_pdf.savefig(pdf_buffer, format='pdf', bbox_inches='tight', pad_inches=0)
pdf_buffer.seek(0)

excel_buffer = generar_excel()

btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    st.download_button(
        label="📥 Descargar Patrón de Corte en PDF (Escala 1:1)",
        data=pdf_buffer,
        file_name=f"Molde_TN_{total_w}x{total_h}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
with btn_col2:
    st.download_button(
        label="📊 Descargar Hoja de Medidas (Excel)",
        data=excel_buffer,
        file_name=f"Medidas_TN_{total_w}x{total_h}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )