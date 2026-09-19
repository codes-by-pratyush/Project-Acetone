# Use an official lightweight Python runtime
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Prevent Python from writing .pyc files and force stdout buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the core application code
COPY . .

# Expose the port FastAPI uses
EXPOSE 8000

# Command to boot the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]