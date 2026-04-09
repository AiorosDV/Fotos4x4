import streamlit as st
from PIL import Image
import requests
import io
import os

# --- CONFIGURACIÓN ---
# Pegá tu clave de remove.bg entre las comillas en la línea de abajo
API_KEY = "PhjdvXY8j4ty4YUSS8YvQjJL"

st.set_page_config(page_title="Creador de Fotos 4x4", layout="centered")

st.title("📸 Creador de Fotos 4x4")
st.write("Subí tu foto y la recortamos automáticamente a 4x4 cm con fondo blanco.")

def process_image(image_input):
    # 1. Preparar la imagen para enviar a remove.bg
    img_byte_arr = io.BytesIO()
    image_input.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # 2. Llamada a la API para borrar fondo y poner blanco
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': img_byte_arr},
        data={'size': 'auto', 'bg_color': 'white'},
        headers={'X-Api-Key': API_KEY},
    )

    if response.status_code == 200:
        img = Image.open(io.BytesIO(response.content))
        
        # 3. LÓGICA DE RECORTE AUTOMÁTICO 4x4
        width, height = img.size
        min_dim = min(width, height)
        
        # Calculamos los bordes para un cuadrado centrado
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2

        # Recortamos y redimensionamos a 400x400 (proporción 4x4)
        img_cropped = img.crop((left, top, right, bottom))
        img_final = img_cropped.resize((400, 400), Image.LANCZOS)
        
        return img_final
    else:
        st.error(f"Error de remove.bg: {response.status_code} - {response.text}")
        return None

# --- INTERFAZ DE USUARIO ---
uploaded_file = st.file_uploader("Elegí una imagen...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)
    st.image(original_image, caption="Imagen Original", use_container_width=True)
    
    if st.button("Procesar Foto 4x4"):
        if API_KEY == "TU_API_KEY_AQUÍ" or API_KEY == "":
            st.warning("⚠️ Por favor, configurá tu API Key en la línea 10 del código.")
        else:
            with st.spinner("Procesando..."):
                result = process_image(original_image)
                if result:
                    st.success("¡Listo!")
                    st.image(result, caption="Resultado 4x4", width=300)
                    
                    # Preparar descarga
                    buf = io.BytesIO()
                    result.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="Descargar Foto 4x4",
                        data=byte_im,
                        file_name="foto_4x4_lista.png",
                        mime="image/png"
                    )
       
