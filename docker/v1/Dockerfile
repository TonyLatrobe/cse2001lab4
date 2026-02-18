FROM python:3.11-alpine

WORKDIR /app

# Install the required dependencies, including the 'requests' library
RUN pip install --no-cache-dir requests

# Copy the application files
COPY app.py .
COPY index.html .

EXPOSE 8080

# Command to run the application
CMD ["python", "app.py"]