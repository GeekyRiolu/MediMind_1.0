from flask import Flask, render_template
import subprocess

app = Flask(__name__)

# Serve the landing page
@app.route('/')
def landing_page():
    return render_template('landing_page.html')

# Redirect to Streamlit app
@app.route('/chatbot')
def chatbot():
    # Run the Streamlit app
    subprocess.Popen(["streamlit", "run", "app.py"])
    return "Redirecting to chatbot..."

if __name__ == '__main__':
    app.run(port=5000)