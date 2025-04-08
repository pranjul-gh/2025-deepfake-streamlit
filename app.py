from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Route for the landing page
@app.route("/")

def home():
    return render_template("index.html")

# Route to handle the button click and run the Streamlit app
@app.route("/run_app", methods=["POST"])
def run_app():
    # Run the Streamlit app using os.system
    os.system("python -m streamlit run Output.py")
    return "Streamlit app is running..."

if __name__ == "__main__":
    app.run()