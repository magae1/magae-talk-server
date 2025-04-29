FROM python:3.13.3-alpine

ARG TURN_CREDENTIAL_DOMAIN
ARG TURN_CREDENTIAL_API_KEY
ENV TURN_CREDENTIAL_DOMAIN=${TURN_CREDENTIAL_DOMAIN}
ENV TURN_CREDENTIAL_API_KEY=${TURN_CREDENTIAL_API_KEY}
ENV PIPENV_VENV_IN_PROJECT=1

# Set working directory
WORKDIR /app

# Copy the Pipfile & Pipfile.lock
COPY Pipfile .
COPY Pipfile.lock .

# Upgrade pip version
RUN python -m pip install --upgrade pip

# Install dependencies
RUN pip install pipenv && pipenv install --system --deploy

# Copy the application code
COPY /src /app

# Expose the port
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]