from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deepfake Detection Service</title>
    <style>
        /* Navigation Bar */
        .nav-container {
            background-color: #002147;
            padding: 10px 20px;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nav-links a {
            color: white;
            margin: 0 15px;
            text-decoration: none;
            font-size: 18px;
        }
        .nav-links a:hover {
            text-decoration: underline;
        }

        /* Hero Section */
        .hero-section {
            background-image: url('https://cdn.pixabay.com/photo/2021/08/17/06/32/detective-6552133_1280.jpg');
            background-size: cover;
            background-position: center;
            padding: 100px;
            text-align: center;
            color: #00879E;
            font-size: 36px;
            font-weight: bold;
        }

        /* Button Styling */
        .hero-button {
            background-color: #ff9800;
            color: white;
            padding: 15px 30px;
            font-size: 20px;
            border: none;
            cursor: pointer;
            border-radius: 8px;
            text-decoration: none;
        }
        .hero-button:hover {
            background-color: #e68900;
        }

        /* Contact Section */
        .contact-section {
            background-color: #f8f8f8;
            padding: 20px;
            text-align: center;
        }
        .contact-info {
            font-size: 18px;
            margin: 5px 0;
        }

        /* About Section */
        .about-section {
            padding: 50px;
            text-align: center;
        }

        /* Center Button */
        .center-button {
            display: flex;
            justify-content: center;
            margin-top: 20px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <!-- Navigation Bar -->
    <div class="nav-container">
        <div><strong>Deepfake Detection Service</strong></div>
        <div class="nav-links">
            <a href="#home">Home</a>
            <a href="#about">About</a>
            <a href="#services">Services</a>
            <a href="#contact">Contact</a>
        </div>
    </div>

    <!-- Hero Section -->
    <div class="hero-section">
        <p>BEST DEEPFAKE DETECTION SERVICE</p>
        <p>Analyze images and videos to detect deepfakes with AI-powered technology</p>
    </div>

    <!-- About Section -->
    <div class="about-section" id="about">
        <h2>About Our Service</h2>
        <p>Our Deepfake Detection Service utilizes state-of-the-art AI models to analyze images and videos, identifying potential manipulations with high accuracy. 
        Built with advanced deep learning techniques, it helps individuals and organizations combat misinformation and digital fraud.</p>
        <p>With a simple and intuitive interface, our tool is designed to make deepfake detection accessible to everyone, from researchers to everyday users.</p>
    </div>

    <!-- Centered "Launch Deepfake Detection" Button -->
    <div class="center-button">
        <form action="/run_app" method="POST">
            <button type="submit" class="hero-button">🚀 Launch Deepfake Detection</button>
        </form>
    </div>

    <!-- Contact Section -->
    <div class="contact-section" id="contact">
        <p class="contact-info"><strong>📞 Contact Us:</strong> +1 888-273-2221</p>
        <p class="contact-info"><strong>📧 Email:</strong> info@deepfake-detection.com</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


# Route to handle the button click and run the Streamlit app
@app.route("/run_app", methods=["POST"])
def run_app():

    # Run the Streamlit app using os.system
    import os
    os.system("python -m streamlit run output.py")
    return 1
    

if __name__ == "__main__":
    app.run(debug=True)