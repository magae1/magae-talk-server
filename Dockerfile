FROM python:3.13.3-alpine

ARG TURN_CREDENTIAL_DOMAIN
ARG TURN_CREDENTIAL_API_KEY
ENV TURN_CREDENTIAL_DOMAIN=${TURN_CREDENTIAL_DOMAIN}
ENV TURN_CREDENTIAL_API_KEY=${TURN_CREDENTIAL_API_KEY}

# Set working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY /src /app

# Expose the port
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]