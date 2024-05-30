# Use the official Python image from the Docker Hub
FROM python:3.8-slim

COPY . /app


# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .


# Expose the port that Streamlit will run on
EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
# Run the Streamlit application
CMD ["app.py"]
