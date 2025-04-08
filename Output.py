import streamlit as st
from PIL import Image
from api import process_image, process_video

# Set the title of your Streamlit app
st.title("🎭 Deepfake Detector")
st.markdown("""
    <style>
        /* Global Background Color */
        body {
            background-color: #e7f3f3;
        }
        .stApp {
            background-color: #e7f3f3;
        }
        /* Title and Subheader Styling */
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #00879E;
            text-align: center;
        }
        .subheader {
            font-size: 20px;
            color: #002147;
            text-align: center;
        }
        /* Button Styling */
        .stButton>button {
            background-color: #ff9800;
            color: white;
            padding: 10px 20px;
            font-size: 18px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #e68900;
        }
        /* Center Button */
        .center-button {
            display: flex;
            justify-content: center;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        /* Result Box Styling */
        .result-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
            text-align: center;
            animation: fadeIn 1s ease-in-out;
        }
        .result {
            font-size: 24px;
            font-weight: bold;
            color: #00879E;
        }
        /* Animation for Result Box */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* Upload Section Styling */
        .upload-section {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        /* Info Section Styling */
        .info-section {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }
        /* Footer Styling */
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #666;
        }
    </style>
""", unsafe_allow_html=True)

# App Description
st.markdown("""
    <div class="subheader">
        Upload an image or video to detect deepfakes using state-of-the-art  models.
    </div>
""", unsafe_allow_html=True)

# File Upload Section
st.markdown("""
    <div class="upload-section">
        <h3>📁 Upload Your File</h3>
    </div>
""", unsafe_allow_html=True)

# Choose between image and video upload
file_type = st.radio("Select file type:", ("Video", "Image"), horizontal=True)

# Upload file through Streamlit
uploaded_file = st.file_uploader(f"Choose a {file_type.lower()}...", type=["jpg", "jpeg", "png", "mp4"])

# Model and Dataset Selection
st.markdown("""
    <div class="upload-section">
        <h3>⚙️ Select Model and Dataset</h3>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    model = st.selectbox("Select Model", ("EfficientNetB4", "EfficientNetB4ST", "EfficientNetAutoAttB4", "EfficientNetAutoAttB4ST"))
with col2:
    dataset = st.radio("Select Dataset", ("DFDC", "FFPP"))

# Threshold Slider
threshold = st.slider("Select Threshold", 0.0, 1.0, 0.5)

# Frames Slider for Video
if file_type == "Video":
    frames = st.slider("Select Frames", 0, 100, 50)

# Display the uploaded file
if uploaded_file is not None:
    if file_type == "Image":
        # Display the uploaded image
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", width=300)
        except Exception as e:
            st.error(f"Error: Invalid Filetype")
    else:
        st.video(uploaded_file)

    # Center the "Check for Deepfake" button
    st.markdown("""
        <div class="center-button">
    """, unsafe_allow_html=True)
    if st.button("🔍 Check for Deepfake"):
        # Convert file to bytes for API request
        if file_type == "Image":
            result, pred = process_image(image=uploaded_file, model=model, dataset=dataset, threshold=threshold)
        else:
            with open(f"uploads/{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.read())
            video_path = f"uploads/{uploaded_file.name}"
            result, pred = process_video(video_path, model=model, dataset=dataset, threshold=threshold, frames=frames)

        # Display the result in a separate box with animation
        st.markdown(
            f'''
            <div class="result-box">
                <h3>The given {file_type} is: <span class="result"> {result} </span> <!-- with a probability of <span class="result">{pred:.2f}</span> --></h3>
            </div>
            ''', unsafe_allow_html=True
        )


        import matplotlib.pyplot as plt
        import numpy as np

        def get_value_from_project(pred):
            """Replace this with your actual function that returns 0-1"""
            return pred # Example value - will show 30% towards "Fake"

        def create_enhanced_real_fake_indicator(value, height=0.8, width=10):
            """Create an enhanced real-fake indicator strip with better visibility"""
            fig, ax = plt.subplots(figsize=(width, height))
            
            # Create gradient from green (Real) to red (Fake)
            gradient = np.linspace(0, 1, 100).reshape(1, -1)
            ax.imshow(gradient, extent=[0, 1, 0, 1], aspect='auto', cmap='RdYlGn_r')
            
            # Add prominent pointer (triangle shape)
            pointer_height = 1.2
            ax.plot([value, value], [0, pointer_height], color='black', linewidth=3)
            ax.plot([value-0.03, value, value+0.03], 
                    [pointer_height, pointer_height+0.2, pointer_height], 
                    color='black', linewidth=3, solid_capstyle='round')
            
            # Add bold labels with better positioning
            ax.text(0, -0.3, "REAL", ha='center', va='center', 
                    fontsize=14, fontweight='bold', color='darkgreen')
            ax.text(1, -0.3, "FAKE", ha='center', va='center', 
                    fontsize=14, fontweight='bold', color='darkred')
            
            # Add current value label above pointer
            ax.text(value, pointer_height+0.3, f"{value:.2f}", 
                    ha='center', va='center', fontsize=12,
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
            
            # Clean up axes
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_frame_on(False)
            plt.tight_layout(pad=0)
            
            return fig

        # Streamlit app
        st.title("confidence for real/fake")
        current_value = get_value_from_project(pred)

        # Create and display the enhanced indicator
        indicator = create_enhanced_real_fake_indicator(current_value)
        st.pyplot(indicator)

        # Optional status message based on value
        if current_value < 0.33:
            st.success("Strong Real characteristics")
        elif current_value > 0.66:
            st.error("Strong Fake characteristics")
        else:
            st.warning("Mixed characteristics")


else:
    st.info("Please upload a file to get started.")

# Project Information Section
st.markdown("""
    <div class="info-section">
        <h3>📚 Project Information</h3>
        <p>This is Final year project of Streamlit app that  takes an image or video as input and predicts whether it is a deepfake or not. It is built using state-of-the-art AI models and deep learning techniques.</p>
        <p>Created by <a href="https://github.com/pranjul-gh/">Pranjul Maurya</a> and <a href="https://github.com/pankil-soni/">Prakash</a>.</p>
        <p>Under the Guidence of: <a href="https://linkedin.com/">Ratan Sir</a> and <a href="https://github.com/pankil-soni/">Anuj Sir</a></p>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>© SRMCEM Deepfake Detector App. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)