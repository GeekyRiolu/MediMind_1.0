# from flask import Flask, render_template
# import subprocess

# app = Flask(__name__)

# # Serve the landing page
# @app.route('/')
# def landing_page():
#     return render_template('landing.html')

# # Redirect to Streamlit app
# @app.route('/chatbot')
# def chatbot():
#     # Run the Streamlit app in the background
#     subprocess.Popen(["streamlit", "run", "app.py"])
    
#     # Return a page with a loading message and JavaScript redirection
#     return '''
#         <html>
#             <head>
#                 <title>Loading MediMind Chatbot...</title>
#                 <style>
#                     .loading {
#                         display: flex;
#                         justify-content: center;
#                         align-items: center;
#                         height: 100vh;
#                         font-size: 24px;
#                         font-family: Arial, sans-serif;
#                     }
#                 </style>
#                 <script>
#                     // Redirect to Streamlit app after 5 seconds
#                     setTimeout(function() {
#                         window.location.href = "http://localhost:8501";
#                     }, 3000); // Adjust the delay as needed
#                 </script>
#             </head>
#             <body>
#                 <div class="loading">
#                     Loading MediMind Chatbot... Please wait.
#                 </div>
#             </body>
#         </html>
#     '''

# if __name__ == '__main__':
#     app.run(port=5000)

# app.py

from flask import Flask, render_template
import subprocess
import threading
import time

app = Flask(__name__)

# Function to start the Streamlit app
def start_streamlit():
    time.sleep(2)  # Simulate a delay for Streamlit to load
    subprocess.run(["streamlit", "run", "app.py"])

@app.route('/')
def landing_page():
    # Render the landing page with a loading indicator
    return render_template('landing.html')

@app.route('/chatbot')
def chatbot():
    # Start the Streamlit app in a separate thread
    threading.Thread(target=start_streamlit).start()
    # Redirect to the Streamlit app after a short delay
    return '''
        <html>
            <head>
                <meta http-equiv="refresh" content="2;url=http://localhost:8501">
                <style>
                    .loading {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        font-size: 24px;
                        font-family: Arial, sans-serif;
                    }
                </style>
            </head>
            <body>
                <div class="loading">
                    Loading MediMind Chatbot...
                </div>
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)