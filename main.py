import streamlit as st
import qrcode
import cv2
from pyzbar.pyzbar import decode
from pathlib import Path
from PIL import Image

# QR Code Generator Function
def generate_qr(data: str, filename: str = "qrcode.png"):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    save_path = Path.cwd() / filename
    img.save(save_path)
    return save_path

# QR Code Decoder Function
def decode_qr(image_path: str):
    img = cv2.imread(image_path)
    decoded_objects = decode(img)

    if not decoded_objects:
        return "[❌] No QR code found in the image."
    
    decoded_data = []
    for obj in decoded_objects:
        decoded_data.append(obj.data.decode('utf-8'))
    return decoded_data

# Streamlit User Interface
def main():
    st.title("QR Code Generator & Decoder")
    
    # Option to choose action: Generate or Decode
    choice = st.radio("Choose an action", ["Generate QR Code", "Decode QR Code"])
    
    if choice == "Generate QR Code":
        # QR Code Generation
        st.subheader("Generate a QR Code")
        text = st.text_input("Enter text or URL to generate QR code:")
        filename = st.text_input("Enter filename to save (e.g., mycode.png):", "qrcode.png")
        
        if st.button("Generate QR Code"):
            if text:
                save_path = generate_qr(text, filename)
                st.image(save_path, caption="Generated QR Code", use_column_width=True)
                st.success(f"QR Code saved as {save_path.name}")
            else:
                st.warning("Please enter some text or URL.")

    elif choice == "Decode QR Code":
        # QR Code Decoding
        st.subheader("Decode a QR Code")
        uploaded_file = st.file_uploader("Upload QR Code image:", type=["png", "jpg", "jpeg"])
        
        if uploaded_file is not None:
            # Read and display the uploaded image
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded QR Code", use_column_width=True)
            
            # Decode the QR code from the image
            with open("temp_qr_image.png", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            decoded_data = decode_qr("temp_qr_image.png")
            if isinstance(decoded_data, list):
                for data in decoded_data:
                    st.success(f"Decoded Data: {data}")
            else:
                st.error(decoded_data)

if __name__ == "__main__":
    main()

