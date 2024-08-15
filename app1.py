import streamlit as st
from PIL import Image
from Encrypt import encode_image
from Decrypt import decode_image
from io import StringIO
from io import BytesIO

# Custom CSS for styling
# Custom CSS for styling the sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #4682B4;
        padding: 20px;
    }
    [data-testid="stSidebar"] h1 {
        color: #FFFFFF;
        font-size: 30px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    [data-testid="stSidebar"] label {
        font-size:50px;
        color: #2F4F4F;
        font-weight:bold;
        padding-left:10px;
    }
    [data-testid="stSidebar"] .stRadio {
        margin-top: 10px;
    }
    .stRadio [role="radio"] {
        background-color: #FFD700;
        color: #FFD700;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 5px;
    }
    .stRadio [role="radio"]:hover {
        background-color: #5D6D7E;
    }
    .stRadio [role="radio"][aria-checked="true"] {
        background-color: #1ABC9C;
        color: #FFFFFF;
        
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with custom title
st.sidebar.title("Shield Quietly")
mode = st.sidebar.radio("Select Operation Mode:", ['Encrypt', 'Decrypt'])
st.markdown('<div class="header" style="font-size:45px;color:#4682B4;font:Italic;"><b><center>Prioritizing Your Privacy Beyond Everything</center></b></div>', unsafe_allow_html=True)
# App title


def extract_text_from_txt(uploaded_file):
    """Extracts text from a .txt file."""
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    return stringio.read()

if mode == 'Encrypt':
    st.markdown('<div class="header" style="font-size:20px;color:#DC143C;font:Italic;"><b><left>Encryption<center><b></div>', unsafe_allow_html=True)
    
    # Option to choose between default image or upload your own
    image_source = st.radio("Choose the image source:", ("Default Image", "Upload Your Own Image"))
    
    if image_source == "Upload Your Own Image":
        uploaded_image = st.file_uploader("Upload an image to encode a message into", type=["png", "jpg", "jpeg"])
    else:
        # Load the default image from your system
        default_image_path = "default_image1.jpeg"  # Provide the correct path to the default image
        uploaded_image = Image.open(default_image_path)
        st.image(uploaded_image, caption="Default Image", use_column_width=True)
    
    # Option to input a message or upload a .txt file
    text_source = st.radio("Choose the message source:", ("Text Input", ".txt File"))
    
    message = None
    if text_source == "Text Input":
        message = st.text_area("Enter the message to encode")
    else:
        uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded_file is not None:
            message = extract_text_from_txt(uploaded_file)
            st.text_area("Text from file:", message, height=200)
    
    # Ask for the encryption key
    encryption_key = st.text_input("Enter an encryption key (will be required for decryption):", type="password")

    if uploaded_image is not None and message and encryption_key:
        image = Image.open(uploaded_image) if image_source == "Upload Your Own Image" else uploaded_image
        if st.button("Encrypt"):
            # Combine message and encryption key
            message_with_key = f"{message}{encryption_key}"
            
            encoded_image = encode_image(image, message_with_key)
            st.image(encoded_image, caption='🔐 Encoded Image', use_column_width=True)
            
            # Save the encoded image to a BytesIO object
            encoded_image_io = BytesIO()
            encoded_image.save(encoded_image_io, format='PNG')
            encoded_image_io.seek(0)
            
            # Provide a download button for the encoded image
            st.download_button(
                label="📥 Download Encoded Image",
                data=encoded_image_io,
                file_name="encoded_image.png",
                mime="image/png"
            )
            
if mode == 'Decrypt':
    st.markdown('<div class="header" style="font-size:20px;color:#DC143C;;font:Italic;"><b><left>Decryption<center><b></div>', unsafe_allow_html=True)
    #st.markdown('<div class="header">Decryption</div>', unsafe_allow_html=True)
    
    # Option to upload an encoded image
    uploaded_image = st.file_uploader("Upload an encoded image", type=["png", "jpg", "jpeg"])
    
    # Ask for the decryption key
    decryption_key = st.text_input("Enter the decryption key:", type="password")
    
    if uploaded_image is not None and decryption_key:
        image = Image.open(uploaded_image)
        if st.button("Decrypt"):
            # Decode the message from the image
            decoded_message_with_key = decode_image(image)
            
            # Extract the original message and verify the key
            if decoded_message_with_key.endswith(decryption_key):
                decoded_message = decoded_message_with_key[:-len(decryption_key)]
                st.text_area("🔓 Decoded Message:", decoded_message, height=200)
                
                # Provide a download button for the decoded message
                st.download_button(
                    label="📥 Download Decoded Message",
                    data=decoded_message,
                    file_name="decoded_message.txt",
                    mime="text/plain"
                )
            else:
                st.error("❌ Incorrect decryption key. Please try again.")

# Footer
st.markdown('<div class="footer">Steganography App - Securely Hide Your Messages in Images</div>', unsafe_allow_html=True)
