# Use the official Python image as a base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port that your app runs on (This line is optional in Heroku)
# EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "--server.port", "$PORT", "front_back_end.py"]
