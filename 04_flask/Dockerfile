# Load python
FROM python:3.11-slim

# Install ssh client and git
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssh-client \
    git && \
    rm -rf /var/lib/apt/lists/*

# set the working directory
WORKDIR /app

# prep the image
RUN python -m pip install --upgrade pip

# expose the port
EXPOSE 5001

# copy files
COPY 04_flask/app.py app.py
COPY 04_flask/requirements.txt requirements.txt
COPY config_public.yaml config_public.yaml
COPY config_private.yaml config_private.yaml
COPY 04_flask/wsgi.py wsgi.py
COPY data data

# install requirements
RUN python -m pip install -r requirements.txt

# copy and install the assistant package
COPY 03_backend recommender
RUN python -m pip install -e recommender

# set the healthcheck
HEALTHCHECK CMD curl --fail http://localhost:5001/health

# set the prod entrypoint
ENTRYPOINT ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5001", "wsgi:app", "--timeout", "300"]