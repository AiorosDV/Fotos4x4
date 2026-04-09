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
