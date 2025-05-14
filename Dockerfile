# Use official Python base image
FROM python:3.10-slim

# Set work directory
WORKDIR /MediMind_1.0

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit and FastAPI ports
EXPOSE 8501
EXPOSE 8000

# Install supervisord to manage both apps
RUN apt-get update && apt-get install -y supervisor && apt-get clean

# Add supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start both apps with supervisor
CMD ["/usr/bin/supervisord"]
