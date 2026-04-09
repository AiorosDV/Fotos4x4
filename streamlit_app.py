
import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Generador de Fotos 4x4", layout="centered")

st.title("📸 Creador de Fotos 4x4")
st.write("Subí tu foto y la preparamos para imprimir en tamaño 4x4 cm.")

uploaded_file = st.file_uploader("Elegí una imagen...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagen Original', use_column_width=True)
    
    # Botón para procesar
    if st.button('Preparar para Impresión'):
        # Definir tamaño 4x4 cm a 300 DPI (aprox 472x472 píxeles)
        size = (472, 472)
        img_4x4 = image.resize(size, Image.LANCZOS)
        
        # Guardar en memoria
        buf = io.BytesIO()
        img_4x4.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.success("¡Imagen lista!")
        st.image(img_4x4, caption='Vista previa 4x4')
        
        st.download_button(
            label="Descargar Foto 4x4",
            data=byte_im,
            file_name="foto_4x4.png",
            mime="image/png"
        )
import streamlit as st
from PIL import Image
import requests
import io
import os

# CONFIGURACIÓN IMPORTANTE
# Reemplaza 'TU_API_KEY_AQUÍ' con tu clave real de remove.bg entre las comillas simples.
# Ejemplo: API_KEY = 'aB1cD2eF3gH4iJ5k'
API_KEY = PhjdvXY8j4ty4YUSS8YvQjJL 

def process_image(image_input, bg_color):
    """
    Borra el fondo y ajusta la imagen a 4x4 (pasaporte/DNI) con color de fondo.
    """
    try:
        if API_KEY == 'TU_API_KEY_AQUÍ':
            st.error("Error: No has puesto tu API Key de remove.bg en el código.")
            return None

        # 1. Borrar el fondo usando remove.bg
        # Convertir la imagen cargada/capturada a bytes para enviarla
        img_byte_arr = io.BytesIO()
        image_input.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': img_byte_arr},
            data={'size': 'auto'}, # Mantiene buena calidad
            headers={'X-Api-Key': API_KEY},
        )

        if response.status_color == 200:
            # Fondo borrado con éxito (imagen PNG transparente)
            img_no_bg = Image.open(io.BytesIO(response.content)).convert("RGBA")
        else:
            st.error(f"Error de remove.bg: {response.status_color} - {response.text}")
            return None

        # 2. Preparar el nuevo fondo y el formato 4x4
        # Dimensiones para pasaporte estándar (aprox. 4cm x 4cm a 300dpi)
        # Usaremos 472x472 píxeles como un estándar común para 4x4cm.
        target_size = (472, 472) 
        
        # Crear la imagen de fondo con el color elegido (RGBA para transparencia inicial)
        final_img = Image.new("RGBA", target_size, bg_color)

        # 3. Ajustar la imagen del sujeto (manteniendo proporción)
        # Redimensionar la imagen sin fondo para que quepa dentro de 4x4, dejando un margen
        max_subject_height = int(target_size[1] * 0.85) # 85% de la altura para la cabeza/hombros
        aspect_ratio = img_no_bg.width / img_no_bg.height
        new_height = min(max_subject_height, img_no_bg.height)
        new_width = int(new_height * aspect_ratio)
        
        # Asegurar que no supere el ancho
        if new_width > target_size[0] * 0.9: # 90% del ancho max
             new_width = int(target_size[0] * 0.9)
             new_height = int(new_width / aspect_ratio)

        img_subject_resized = img_no_bg.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # 4. Pegar el sujeto centrado sobre el fondo de color
        paste_x = (target_size[0] - new_width) // 2
        paste_y = (target_size[1] - new_height) // 2 # Centrado vertical simple
        # Para DNI a veces se prefiere un poco más arriba, pero centrado es más seguro
        
        final_img.paste(img_subject_resized, (paste_x, paste_y), img_subject_resized)

        # Convertir a RGB (sacar transparencia) para guardar como JPEG (estándar DNI)
        final_img_rgb = final_img.convert("RGB")
        
        return final_img_rgb

    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
        return None

# --- Interfaz de Streamlit ---
st.set_page_config(page_title="Creador Foto DNI 4x4", page_icon="📸")

st.title("📸 Creador de Foto DNI/Pasaporte 4x4")
st.write("Saca una foto o sube una imagen para crear tu foto de 4x4cm con fondo de color.")

# --- SECCIÓN 1: Clave API (Para facilidad del usuario, mejor usar Secrets en producción) ---
# (Opcional) Puedes ocultar esto si ya editaste el código arriba
st.sidebar.header("Configuración")
st.sidebar.write("Para que funcione el borrado de fondo, necesitas la clave API de remove.bg.")
user_api_key = st.sidebar.text_input("Ingresa tu API Key aquí (o edítala en el código):", type="password")
if user_api_key:
    API_KEY = user_api_key # Prioriza la clave ingresada en la interfaz

# --- SECCIÓN 2: Opciones de Fondo ---
st.subheader("1. Elige el color de fondo")
col1, col2 = st.columns(2)
with col1:
    bg_color_name = st.radio("Color:", ("Blanco", "Celeste"))

# Mapeo de nombres a valores de color (RGBA)
color_map = {
    "Blanco": (255, 255, 255, 255),
    "Celeste": (135, 206, 235, 255) # Un celeste estándar
}
selected_bg_color = color_map[bg_color_name]


# --- SECCIÓN 3: Entrada de Imagen ---
st.subheader("2. Saca o Sube tu Foto")

# Opción 1: Cámara del teléfono (camera_input)
cam_image = st.camera_input("Sacar foto con la cámara")

# Opción 2: Subir archivo (file_uploader)
file_image = st.file_uploader("O sube una foto existente...", type=["jpg", "jpeg", "png"])

input_image = None
image_source = None

# Prioridad: Si sacó foto con la cámara, usa esa. Sino, la subida.
if cam_image is not None:
    input_image = Image.open(cam_image)
    image_source = "Cámara"
elif file_image is not None:
    input_image = Image.open(file_image)
    image_source = "Archivo"

# --- SECCIÓN 4: Procesamiento y Resultados ---
if input_image is not None:
    st.write(f"Imagen detectada desde: {image_source}")
    st.image(input_image, caption="Imagen Original", use_column_width=True)

    # Botón para iniciar el proceso
    if st.button(f"Crear Foto 4x4 con fondo {bg_color_name}"):
        with st.spinner('Procesando... borrando fondo y ajustando tamaño (esto usa remove.bg)...'):
            processed_img = process_image(input_image, selected_bg_color)

        if processed_img:
            st.subheader("3. ¡Tu Foto 4x4 está lista!")
            
            # Mostrar resultado centrada y con borde simulando el recorte 4x4
            st.image(processed_img, caption=f"Foto Pasaporte 4x4cm ({bg_color_name})", width=300)

            # Botón para descargar
            # Convertir PIL Image a bytes para la descarga
            buf = io.BytesIO()
            processed_img.save(buf, format="JPEG")
            byte_im = buf.getvalue()

            st.download_button(
                label="Descargar Foto 4x4 (JPEG)",
                data=byte_im,
                file_name=f"foto_dni_4x4_{bg_color_name.lower()}.jpg",
                mime="image/jpeg"
            )
            st.success("¡Listo! Ya puedes descargar tu foto.")

st.write("---")
st.caption("Nota: Esta aplicación utiliza el servicio remove.bg. Asegúrate de tener créditos disponibles en tu cuenta.")
