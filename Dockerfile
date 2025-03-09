# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim-bullseye

# Copy local code to the container image.
ENV APP_HOME=/src
ENV PYTHONUNBUFFERED=True
WORKDIR $APP_HOME

# Install Python dependencies and Gunicorn
ADD requirements.txt .
RUN apt-get update && apt-get install -y gcc 
RUN apt-get install -y g++
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir gunicorn
RUN groupadd -r app && useradd -r -g app app

# Copy the rest of the codebase into the image
COPY --chown=app:app . ./
USER app
# RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir gunicorn
# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available in Cloud Run.
EXPOSE 8080
# CMD ['exec gunicorn' '--bind :$PORT' '--log-level info' '--workers 1' '--threads 8' '--timeout 0' 'app:server']
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--log-level", "info", "--workers", "1", "--threads", "8", "--timeout", "0", "src.app:server"]

# CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "src.app:server"]