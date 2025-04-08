# from flask import Flask, render_template, request
# import os

# app = Flask(__name__)

# # Route for the landing page
# @app.route("/")
# def home():
#     return render_template("index.html")

# # Route to handle the button click and run the Streamlit app
# @app.route("/run_app", methods=["POST"])
# def run_app():
#     # Run the Streamlit app using os.system
#     os.system("python -m streamlit run Output.py")
#     return "Streamlit app is running..."

# if __name__ == "__main__":
#     app.run()


import streamlit as st
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