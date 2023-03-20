FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
