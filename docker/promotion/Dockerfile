FROM python:3.11-alpine

# Install the Kubernetes client and other dependencies
RUN pip install --no-cache-dir kubernetes

# Set working directory
WORKDIR /app

# Copy the promotion server script into the container
COPY promotion_server.py .

# Expose the port the application will run on
EXPOSE 5000

# Define the command to run the promotion server
CMD ["python", "promotion_server.py"]