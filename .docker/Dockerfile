# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12.3

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN python -m pip install --upgrade pip
RUN python -m pip install pip-tools
COPY requirements/base.in ./requirements.in
RUN python -m piptools compile ./requirements.in -o requirements.txt
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY ./shared /app/shared
COPY ./fast_api /app/fast_api
COPY ./models /app/models

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "fast_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
