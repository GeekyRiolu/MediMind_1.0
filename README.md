

---

# MediMind - AI-Powered Clinic Assistant

MediMind is an AI-powered healthcare assistant designed to streamline medical tasks such as processing patient EHR data, summarizing medical text, and generating medical advice. Built on a **Multi-Agent AI Architecture**, this application leverages advanced AI models to assist healthcare professionals.

---

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Setup Instructions](#setup-instructions)
   - [Step 1: Clone the Repository](#step-1-clone-the-repository)
   - [Step 2: Create a Virtual Environment](#step-2-create-a-virtual-environment)
   - [Step 3: Activate the Virtual Environment](#step-3-activate-the-virtual-environment)
   - [Step 4: Install Requirements](#step-4-install-requirements)
   - [Step 5: Run the Flask Application](#step-5-run-the-flask-application)
4. [Project Structure](#project-structure)
5. [Contributing](#contributing)
6. [License](#license)

---


## Features
The **Clinic Agent** is the core feature of MediMind, designed to assist healthcare professionals in processing and analyzing patient EHR data. Here’s what it can do:

- **Process EHR Data**: Analyze patient Electronic Health Records (EHR) to extract key insights.
- **Generate Medical Advice**: Provide actionable medical advice based on the patient’s EHR data.
- **Summarize Patient Data**: Create concise summaries of patient histories, diagnoses, and treatment plans.
- **Sanitize PHI**: Remove or anonymize Protected Health Information (PHI) to ensure compliance with privacy regulations.
- **Interactive Interface**: A user-friendly interface for healthcare professionals to interact with the Clinic Agent.


---

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- `pip` (Python package manager)
- Git (for cloning the repository)

---

## Setup Instructions

### Step 1: Clone the Repository
Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/GeekyRiolu/MediMind_1.0.git
cd MediMind_1.0
```

---

### Step 2: Create a Virtual Environment
Create a virtual environment to isolate the project dependencies:

```bash
python -m venv venv
```

---

### Step 3: Activate the Virtual Environment
Activate the virtual environment:

- **On Windows**:
  ```bash
  venv\Scripts\activate
  ```

- **On macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

Once activated, your terminal prompt should change to indicate the virtual environment is active.

---

### Step 4: Install Requirements
Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

---

### Step 5: Run the Application
Start the FastAPI application by running the following command: (landing page)

```bash
cd MediMind_1.0
uvicorn fastapi_app:app --reload 
```
For Running Chatbot UI directly:

```bash
streamlit run app.py
```

Run the dockerized app:

```bash
docker build -t medimind-app .
docker run -p 8001:8000 -p 8501:8501 medimind-app
```

Visit in your browser:
- FastAPI Landing Page: http://localhost:8000 (It automatically redirects to 8501 port)
- Chatbot Interface: http://localhost:8501

---

## Project Structure
Here’s an overview of the project structure:

```
MediMind_1.0/
├── app.py                  # Main Streamlit application
├── flask_app.py            # Main Flask application
├── requirements.txt        # List of dependencies
├── README.md               # Project documentation
├── venv/                   # Virtual environment (ignored in .gitignore)
├── agents/                 # AI agents for various tasks
│   ├── __init__.py
│   ├── clinic_agent.py
│   ├── follow_up_agent.py
│   └── ...
├── utils/                  # Utility functions and helpers
│   ├── logger.py
│   └── ...
└── template/                 # Template files (CSS, JS, images)
    ├── landing_page.html
    └── ...
```

---

## Contributing
We welcome contributions to MediMind! If you’d like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push them to your fork.
4. Submit a pull request with a detailed description of your changes.

---

## Contact
For any questions or feedback, feel free to reach out:
- **Email**: rishabh667788@gmail.com
- **GitHub**: [GeekyRiolu](https://github.com/GeekyRiolu)

---

Enjoy using **MediMind**! 🚀

---
