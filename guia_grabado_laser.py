import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from fpdf import FPDF
import tempfile

st.set_page_config(page_title="Guía Grabado Láser TONAL", page_icon="🎯", layout="centered")

def generar_pdf_1_1(ancho_pieza, alto_pieza, ancho_logo, alto_logo, x_origen, y_origen):
    # FPDF trabaja en milímetros
    pdf = FPDF(unit='mm', format='A4')
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Guia de Grabado Laser - TONAL", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Medidas de la pieza: {ancho_pieza} x {alto_pieza} cm", ln=True)
    pdf.cell(0, 8, f"Medidas del logotipo: {ancho_logo} x {alto_logo} cm", ln=True)
    pdf.cell(0, 8, f"Origen del laser (desde inf-izq): X = {x_origen:.2f} cm, Y = {y_origen:.2f} cm", ln=True)
    pdf.ln(10)
    
    # Dibujo a escala 1:1
    offset_x = 20  # Margen izquierdo en el papel (mm)
    offset_y = 50  # Margen superior en el papel (mm)
    
    w_pieza_mm = ancho_pieza * 10
    h_pieza_mm = alto_pieza * 10
    w_logo_mm = ancho_logo * 10
    h_logo_mm = alto_logo * 10
    
    # Contorno de la pieza (Color Sepia Nogalina: #6E5A44 -> RGB: 110, 90, 68)
    pdf.set_draw_color(110, 90, 68)
    pdf.rect(offset_x, offset_y, w_pieza_mm, h_pieza_mm)
    
    # Coordenadas del logo
    logo_x_mm = offset_x + (x_origen * 10)
    # FPDF dibuja de arriba hacia abajo, invertimos el origen Y
    logo_y_mm = offset_y + h_pieza_mm - (y_origen * 10) - h_logo_mm
    
    # Relleno del logo (Azul Prusia: #1D2951 -> RGB: 29, 41, 81)
    pdf.set_fill_color(29, 41, 81)
    pdf.rect(logo_x_mm, logo_y_mm, w_logo_mm, h_logo_mm, style='F')
    
    # Generar bytes usando un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        with open(tmp.name, "rb") as f:
            return f.read()

st.title("🎯 Calculadora de Posicionamiento Láser")
st.markdown("Ajusta las medidas para encontrar el punto de origen del logotipo y exportar la guía a escala 1:1.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Medidas de la Pieza (cm)")
    ancho_pieza = st.number_input("Ancho total", min_value=1.0, value=11.0, step=0.5)
    alto_pieza = st.number_input("Alto total", min_value=1.0, value=21.0, step=0.5)

    st.subheader("2. Dimensiones del Logo (cm)")
    ancho_logo = st.number_input("Ancho del logotipo", min_value=0.1, value=2.5, step=0.1)
    alto_logo = st.number_input("Alto del logotipo", min_value=0.1, value=2.5, step=0.1)

with col2:
    st.subheader("3. Posición en el Cuero")
    
    centrado_h = st.checkbox("Centrar horizontalmente", value=True)
    if not centrado_h:
        margen_izq = st.number_input("Distancia desde izquierda (cm)", min_value=0.0, value=1.0, step=0.1)
    else:
        margen_izq = (ancho_pieza - ancho_logo) / 2
        st.info(f"Margen izquierdo: **{margen_izq:.2f} cm**")

    centrado_v = st.checkbox("Centrar verticalmente", value=False)
    if not centrado_v:
        margen_inf = st.number_input("Distancia desde abajo (cm)", min_value=0.0, value=3.0, step=0.1)
    else:
        margen_inf = (alto_pieza - alto_logo) / 2
        st.info(f"Margen inferior: **{margen_inf:.2f} cm**")

# Coordenadas
x_origen = margen_izq
y_origen = margen_inf

st.divider()
st.subheader("📍 Coordenadas de Origen y Exportación")
st.markdown(f"Coloca el punto de origen de tu láser a **{x_origen:.2f} cm** de la izquierda y a **{y_origen:.2f} cm** desde abajo.")

# Botón de Descarga PDF
pdf_bytes = generar_pdf_1_1(ancho_pieza, alto_pieza, ancho_logo, alto_logo, x_origen, y_origen)
st.download_button(
    label="📄 Descargar Guía en PDF (Escala 1:1)",
    data=pdf_bytes,
    file_name="guia_laser_tonal.pdf",
    mime="application/pdf",
    type="primary"
)

# Visualización Gráfica
fig, ax = plt.subplots(figsize=(5, 7))
pieza = patches.Rectangle((0, 0), ancho_pieza, alto_pieza, linewidth=2, edgecolor='#6E5A44', facecolor='#FAF3E6', label='Pieza de cuero')
ax.add_patch(pieza)
logo = patches.Rectangle((x_origen, y_origen), ancho_logo, alto_logo, linewidth=0, facecolor='#1D2951', label='Logotipo')
ax.add_patch(logo)

if centrado_h: ax.axvline(x=ancho_pieza/2, color='gray', linestyle='--', alpha=0.5)
if centrado_v: ax.axhline(y=alto_pieza/2, color='gray', linestyle='--', alpha=0.5)

ax.set_xlim(-1, ancho_pieza + 1)
ax.set_ylim(-1, alto_pieza + 1)
ax.set_aspect('equal')
ax.legend(loc='upper right')
plt.title("Previsualización Web")
plt.xlabel("Ancho (cm)")
plt.ylabel("Alto (cm)")
plt.grid(True, linestyle=':', alpha=0.4)

st.pyplot(fig)
