# Use the official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Copy the entire app directory to /app
COPY app/ app/

# Create the logs directory and volume
RUN mkdir -p app/logs /volume

# Expose port 80
EXPOSE 80

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
