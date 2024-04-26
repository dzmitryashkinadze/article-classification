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
EXPOSE 8501

# copy files
COPY 05_streamlit/app.py app.py
COPY 05_streamlit/requirements.txt requirements.txt
COPY config_public.yaml config_public.yaml
COPY config_private.yaml config_private.yaml

# install requirements
RUN python -m pip install -r requirements.txt

# set the healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# set the prod entrypoint
ENTRYPOINT ["python", "-m", "streamlit", "run", "app.py", "--server.port", "8501"]