# Base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY ./portfolio_manager .

# Expose port for the application
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED 1