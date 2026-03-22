import streamlit as st
from PIL import Image, ImageOps
import random
import io
import zipfile

# Page ka title aur description
st.title("Bulk Image Border Generator 🖼️")
st.write("Apni 100 images upload karein aur automatic random color borders ke saath ZIP file download karein.")

# Border ki motai set karne ka option UI me
border_thickness = st.number_input("Border ki motai (pixels mein) set karein:", min_value=1, max_value=200, value=25)

# Multiple images upload karne ka button
uploaded_files = st.file_uploader("Apni images yahan upload karein", type=['png', 'jpg', 'jpeg', 'webp'], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} images upload ho gayi hain!")
    
    # Process karne ka button
    if st.button("Generate Images & Create ZIP"):
        # Memory mein zip file banane ke liye
        zip_buffer = io.BytesIO()
        
        with st.spinner("Images process ho rahi hain... Please wait!"):
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for i, uploaded_file in enumerate(uploaded_files):
                    try:
                        # Image read karein
                        img = Image.open(uploaded_file)
                        
                        # Random color banayein (RGB format me)
                        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        
                        # Image par border lagayein
                        bordered_img = ImageOps.expand(img, border=int(border_thickness), fill=random_color)
                        
                        # Agar PNG (transparent) hai toh JPEG me save karne ke liye RGB me convert karein
                        if bordered_img.mode in ("RGBA", "P"):
                            bordered_img = bordered_img.convert("RGB")
                            
                        # Processed image ko memory me save karein
                        img_byte_arr = io.BytesIO()
                        bordered_img.save(img_byte_arr, format='JPEG')
                        img_byte_arr.seek(0)
                        
                        # Zip file ke andar image ko save karna
                        new_filename = f"bordered_image_{i+1}.jpg"
                        zip_file.writestr(new_filename, img_byte_arr.read())
                        
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {e}")

        # Download button ke liye zip file ready karna
        zip_buffer.seek(0)
        st.success("Aapki ZIP file ready hai!")
        
        st.download_button(
            label="📦 Download All Images (ZIP)",
            data=zip_buffer,
            file_name="meesho_bordered_images.zip",
            mime="application/zip"
        )