FROM python:3.9-slim

WORKDIR /app

# Copy the requirements.txt from App and install dependencies
COPY ./App/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the entire App directory and the Database directory
COPY ./App /app
COPY ./App/Database /app/Database

# Expose port 5000
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
