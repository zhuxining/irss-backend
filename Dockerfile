FROM python:3.11

# Set the working directory inside the container to /irss/
WORKDIR /irss-backend

# Copy the requirements.lock file from the host machine to the container's /irss/ directory
COPY ./requirements.lock ./requirements.lock

# Install all required Python packages listed in requirements.lock using pip
RUN pip install --no-cache-dir --upgrade -r /irss/requirements.lock

# Copy the app directory from the host machine to the container's /irss/ directory
COPY ./app /irss-backend/app

# Start Uvicorn with our main FastAPI app on 0.0.0.0:80 inside the container
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80","--reload"]