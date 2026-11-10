import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

st.set_page_config(page_title="Calculadora TN TONAL", layout="wide")

st.title("Calculadora de Patrones TN (Standard & Trifold)")

# --- SELECTOR DE MODELO ---
modelo_tn = st.radio("Selecciona el tipo de cubierta:", ["Modelo Estándar (Doble doblez)", "Modelo Trifold (Triple doblez)"], horizontal=True)
st.divider()

# =========================================================================
# ==================== LÓGICA: MODELO ESTÁNDAR ============================
# =========================================================================
if modelo_tn == "Modelo Estándar (Doble doblez)":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**1. Inserto y Ajustes**")
        insert_w = st.number_input("Ancho del Inserto (cm)", value=10.5, step=0.1, key="std_w")
        insert_h = st.number_input("Alto del Inserto (cm)", value=14.8, step=0.1, key="std_h")
        spine_w = st.number_input("Ancho del Lomo (cm)", value=1.5, step=0.1, key="std_spine")
    
    with col2:
        st.markdown("**2. Holguras**")
        margin_x = st.number_input("Margen Lateral (cm)", value=0.5, step=0.1, key="std_mx")
        margin_y = st.number_input("Margen Superior/Inferior (cm)", value=0.6, step=0.1, key="std_my")
    
    with col3:
        st.markdown("**3. Solapa Interior (Izquierda)**")
        incluir_solapa = st.checkbox("Incluir solapa y costura", value=True, key="std_solapa")
        flap_w = st.number_input("Ancho de la solapa (cm)", value=8.5, step=0.1, key="std_flap") if incluir_solapa else 0

    total_w = round(margin_x + insert_w + spine_w + insert_w + margin_x, 1)
    total_h = round(margin_y + insert_h + margin_y, 1)

    st.success(f"**PIEZA PRINCIPAL:** Cortar cuero a {total_w} cm de ancho x {total_h} cm de alto")
    if incluir_solapa:
        st.info(f"**SOLAPA INTERIOR:** Cortar cuero a {flap_w} cm de ancho x {total_h} cm de alto")

    def generar_grafico(formato="png"):
        espacio_entre_piezas = 2 if incluir_solapa else 0
        fig_w = total_w + espacio_entre_piezas + flap_w if incluir_solapa else total_w
        fig_h = total_h
        
        dpi = 300 if formato in ["pdf", "svg"] else 100
        fig, ax = plt.subplots(figsize=(fig_w / 2.54, fig_h / 2.54), dpi=dpi)
        ax.set_xlim(0, fig_w)
        ax.set_ylim(0, fig_h)
        ax.axis('off')
        
        if formato in ["pdf", "svg"]:
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)

        ax.add_patch(patches.Rectangle((0, 0), total_w, total_h, linewidth=1, edgecolor='black', facecolor='none'))
        center_x, center_y = total_w / 2, total_h / 2
        
        # Elástico (2 mm)
        radio_el = 0.1
        y_holes = [center_y, total_h - 1.0, total_h - 1.8, 1.0, 1.8]
        for y in y_holes:
            ax.add_patch(patches.Circle((center_x, y), radio_el, facecolor='black', edgecolor='none', linewidth=0))

        # Costura (1.2 mm)
        if incluir_solapa:
            stitch_r = 0.06
            margen_c = 0.4
            sep_c = 0.6
            
            def get_evenly_spaced_coords(start, end, target_step):
                L = end - start
                if L <= 0: return []
                num_steps = max(1, int(round(L / target_step)))
                return np.linspace(start, end, num_steps + 1)

            y_costura = get_evenly_spaced_coords(margen_c, total_h - margen_c, sep_c)
            x_coords_full = get_evenly_spaced_coords(margen_c, flap_w - margen_c, sep_c)
            x_costura_horiz = x_coords_full[1:] if len(x_coords_full) > 1 else []

            # Costura base
            for y in y_costura: ax.add_patch(patches.Circle((margen_c, y), stitch_r, facecolor='black', edgecolor='none', linewidth=0))
            for x in x_costura_horiz:
                ax.add_patch(patches.Circle((x, total_h - margen_c), stitch_r, facecolor='black', edgecolor='none', linewidth=0))
                ax.add_patch(patches.Circle((x, margen_c), stitch_r, facecolor='black', edgecolor='none', linewidth=0))

            # Solapa
            offset_x = total_w + espacio_entre_piezas
            ax.add_patch(patches.Rectangle((offset_x, 0), flap_w, total_h, linewidth=1, edgecolor='black', facecolor='none'))
            for y in y_costura: ax.add_patch(patches.Circle((offset_x + margen_c, y), stitch_r, facecolor='black', edgecolor='none', linewidth=0))
            for x in x_costura_horiz:
                ax.add_patch(patches.Circle((offset_x + x, total_h - margen_c), stitch_r, facecolor='black', edgecolor='none', linewidth=0))
                ax.add_patch(patches.Circle((offset_x + x, margen_c), stitch_r, facecolor='black', edgecolor='none', linewidth=0))

        return fig

# =========================================================================
# ==================== LÓGICA: MODELO TRIFOLD =============================
# =========================================================================
elif modelo_tn == "Modelo Trifold (Triple doblez)":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**1. Base del Trifold**")
        insert_w = st.number_input("Ancho del Inserto Base (cm)", value=10.5, step=0.1, key="tri_w")
        insert_h = st.number_input("Alto del Inserto (cm)", value=14.8, step=0.1, key="tri_h")
        factor_w = st.number_input("Factor Multiplicador de Ancho", value=3.2, step=0.1, help="Para tamaño A6 usar ~3.2")
    
    with col2:
        st.markdown("**2. Holguras y Perforaciones**")
        margin_y = st.number_input("Margen Superior/Inferior (cm)", value=1.1, step=0.1, key="tri_my")
        dist_lomo = st.number_input("Distancia al primer lomo (cm)", value=12.0, step=0.1, help="De izquierda a derecha")
        
    with col3:
        st.markdown("**3. Solapa Interior (Izquierda)**")
        incluir_solapa = st.checkbox("Incluir solapa y costura", value=True, key="tri_solapa")
        flap_w = st.number_input("Ancho de la solapa (cm)", value=8.5, step=0.1, key="tri_flap") if incluir_solapa else 0

    # Cálculo Trifold
    total_w = round(insert_w * factor_w, 1)
    total_h = round(margin_y + insert_h + margin_y, 1)

    st.success(f"**CUBIERTA TRIFOLD:** Cortar cuero a {total_w} cm de ancho x {total_h} cm de alto")
    if incluir_solapa:
        st.info(f"**SOLAPA INTERIOR:** Cortar cuero a {flap_w} cm de ancho x {total_h} cm de alto")

    def generar_grafico(formato="png"):
        espacio_entre_piezas = 2 if incluir_solapa else 0
        fig_w = total_w + espacio_entre_piezas + flap_w if incluir_solapa else total_w
        fig_h = total_h
        
        dpi = 300 if formato in ["pdf", "svg"] else 100
        fig, ax = plt.subplots(figsize=(fig_w / 2.54, fig_h / 2.54), dpi=dpi)
        ax.set_xlim(0, fig_w)
        ax.set_ylim(0, fig_h)
        ax.axis('off')
        if formato in ["pdf", "svg"]: plt.subplots_adjust(left=0, right=1, bottom=0, top=1)

        # Perímetro Trifold Principal
        ax.add_patch(patches.Rectangle((0, 0), total_w, total_h, linewidth=1, edgecolor='black', facecolor='none'))
        
        # --- PERFORACIONES PARA ELÁSTICOS (Diámetro 2mm) ---
        radio_el = 0.1
        
        # Columnas de lomo (Separadas por 8mm = 0.8cm)
        spine_1_x = dist_lomo
        spine_2_x = dist_lomo + 0.8
        
        # Coordenadas Y para los lomos (A 8mm y 16mm de los bordes superior e inferior)
        y_holes = [total_h - 0.8, total_h - 1.6, 0.8, 1.6]
        
        for y in y_holes:
            ax.add_patch(patches.Circle((spine_1_x, y), radio_el, facecolor='black', edgecolor='none', linewidth=0))
            ax.add_patch(patches.Circle((spine_2_x, y), radio_el, facecolor='black', edgecolor='none', linewidth=0))

        # Hoyos centrales para elástico de cierre (Separados por 16mm = 1.6cm)
        ax.add_patch(patches.Circle((spine_1_x, total_h / 2), radio_el, facecolor='black', edgecolor='none', linewidth=0))
        ax.add_patch(patches.Circle((spine_1_x + 1.6, total_h / 2), radio_el, facecolor='black', edgecolor='none', linewidth=0))

        # --- SOLAPA Y COSTURA ---
        if incluir_solapa:
            stitch_r = 0.06
            margen_c = 0.4
            sep_c = 0.6
            
            def get_evenly_spaced_coords(start, end, target_step):
                L = end - start
                if L <= 0: return []
                num_steps = max(1, int(round(L / target_step)))
                return np.linspace(start, end, num_steps + 1)

            y_costura = get_evenly_spaced_coords(margen_c, total_h - margen_c, sep_c)
            x_coords_full = get_evenly_spaced_coords(margen_c, flap_w - margen_c, sep_c)
            x_costura_horiz = x_coords_full[1:] if len(x_coords_full) > 1 else []

            # Costura base principal (solo zona de solapa izquierda)
            for y in y_costura: 
                ax.add_patch(patches.Circle((margen_c, y), stitch_r, facecolor='black', edgecolor='none', linewidth=0))
            for x in x_costura_horiz:
                ax.add_patch(patches.Circle((x, total_h - margen_c), stitch_r, facecolor='black', edgecolor='none', linewidth=0))
                ax.add_patch(patches.Circle((x, margen_c), stitch_r, facecolor='black', edgecolor='none', linewidth=0))

            # Dibujo de Solapa separada
            offset_x = total_w + espacio_entre_piezas
            ax.add_patch(patches.Rectangle((offset_x, 0), flap_w, total_h, linewidth=1, edgecolor='black', facecolor='none'))
            for y in y_costura: 
                ax.add_patch(patches.Circle((offset_x + margen_c, y), stitch_r, facecolor='black', edgecolor='none', linewidth=0))
            for x in x_costura_horiz:
                ax.add_patch(patches.Circle((offset_x + x, total_h - margen_c), stitch_r, facecolor='black', edgecolor='none', linewidth=0))
                ax.add_patch(patches.Circle((offset_x + x, margen_c), stitch_r, facecolor='black', edgecolor='none', linewidth=0))

        return fig


# =========================================================================
# ==================== EXPORTACIÓN MULTIFORMATO ===========================
# =========================================================================
st.divider()
st.markdown(f"**Vista Previa del Patrón - {modelo_tn}**")

fig_visual = generar_grafico(formato="png")
st.pyplot(fig_visual)

# Generar PDF
fig_pdf = generar_grafico(formato="pdf")
pdf_buffer = io.BytesIO()
fig_pdf.savefig(pdf_buffer, format='pdf', bbox_inches='tight', pad_inches=0)
pdf_buffer.seek(0)

# Generar SVG (Vector puro)
fig_svg = generar_grafico(formato="svg")
svg_buffer = io.BytesIO()
fig_svg.savefig(svg_buffer, format='svg', bbox_inches='tight', pad_inches=0)
svg_buffer.seek(0)

btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    st.download_button(
        label="📥 Descargar Patrón (PDF)",
        data=pdf_buffer,
        file_name=f"TN_{total_w}x{total_h}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
with btn_col2:
    st.download_button(
        label="✒️ Descargar Vector (SVG)",
        data=svg_buffer,
        file_name=f"TN_Vectores_{total_w}x{total_h}.svg",
        mime="image/svg+xml",
        use_container_width=True
    )

# Generar Excel
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
    ws['B2'].value, ws['B2'].font, ws['B2'].alignment = f"CALCULADORA DE MEDIDAS - {modelo_tn.upper()} (TONAL)", Font(size=12, bold=True, color="1F497D"), c_align
    
    headers = ["Parámetro", "Valor (cm)", "Descripción"]
    for col_num, header in enumerate(headers, start=2):
        cell = ws.cell(row=4, column=col_num, value=header)
        cell.fill, cell.font, cell.alignment, cell.border = dark_blue_fill, white_font, c_align, b_style

    if modelo_tn == "Modelo Estándar (Doble doblez)":
        data = [
            ("Ancho del Inserto", insert_w, "Ancho del cuadernillo cerrado"),
            ("Alto del Inserto", insert_h, "Alto del cuadernillo cerrado"),
            ("Ancho del Lomo", spine_w, "Espacio central para elásticos/cuadernillos"),
            ("Margen Lateral", margin_x, "Holgura izquierda y derecha"),
            ("Margen Superior/Inferior", margin_y, "Holgura arriba y abajo"),
            ("Ancho Solapa", flap_w if incluir_solapa else 0, "Ancho de la solapa interior izquierda")
        ]
        formulas = [
            ("Ancho Bruto", "=C5+C5+C7+C8+C8", "Inserto + Inserto + Lomo + Margen(x2)"),
            ("Alto Bruto", "=C6+C9+C9", "Inserto + Margen Sup/Inf(x2)"),
            ("ANCHO DE CORTE FINAL", "=C13", "Medida exacta al decimal"),
            ("ALTO DE CORTE FINAL", "=C14", "Medida exacta al decimal"),
            ("SOLAPA INTERIOR (Ancho x Alto)", '=C10 & " x " & C16', "Ancho de solapa x Alto de corte")
        ]
    else:
        data = [
            ("Ancho del Inserto Base", insert_w, "Ancho del cuadernillo cerrado"),
            ("Factor Multiplicador", factor_w, "Proporción para el ancho total"),
            ("Alto del Inserto", insert_h, "Alto del cuadernillo cerrado"),
            ("Margen Superior/Inferior", margin_y, "Holgura arriba y abajo"),
            ("Distancia Primer Lomo", dist_lomo, "Distancia desde borde izquierdo"),
            ("Ancho Solapa", flap_w if incluir_solapa else 0, "Ancho de la solapa interior izquierda")
        ]
        formulas = [
            ("Ancho Bruto", "=C5*C6", "Inserto Base x Factor Multiplicador"),
            ("Alto Bruto", "=C7+C8+C8", "Inserto + Margen Sup/Inf(x2)"),
            ("ANCHO DE CORTE FINAL", "=C13", "Medida exacta al decimal"),
            ("ALTO DE CORTE FINAL", "=C14", "Medida exacta al decimal"),
            ("SOLAPA INTERIOR (Ancho x Alto)", '=C10 & " x " & C16', "Ancho de solapa x Alto de corte")
        ]

    for row_num, row_data in enumerate(data, start=5):
        for col_num, value in enumerate(row_data, start=2):
            cell = ws.cell(row=row_num, column=col_num, value=value)
            cell.border, cell.alignment = b_style, (c_align if col_num == 3 else l_align)
            if row_num % 2 == 0: cell.fill = light_blue_fill

    ws.merge_cells('B12:E12')
    ws['B12'].value, ws['B12'].font, ws['B12'].fill, ws['B12'].alignment = "CÁLCULO DE CORTE FINAL", Font(size=12, bold=True, color="FFFFFF"), dark_blue_fill, c_align

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

excel_buffer = generar_excel()
with btn_col3:
    st.download_button(
        label="📊 Descargar Medidas (Excel)",
        data=excel_buffer,
        file_name=f"Medidas_TN_{total_w}x{total_h}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
