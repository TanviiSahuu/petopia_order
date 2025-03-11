# Use a lightweight Python image
FROM python:3.9-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .  
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port 8001 (assuming pet_order service runs on this port)
EXPOSE 8001

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
