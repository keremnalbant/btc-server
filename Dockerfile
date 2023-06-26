# Set base image (host OS)
FROM python:3.10-buster
WORKDIR /app
COPY ./requirements.txt .

RUN apt-get update && apt-get install -y gcc make git dh-python libpython3-dev libpython3.7 libpython3.7-dev python3-dev

# By default, listen on port 5000
EXPOSE 5000

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY ./ .

# Specify the command to run on container start
ENTRYPOINT ["uvicorn", "main:app", "--proxy-headers", "--forwarded-allow-ips", "*", "--host", "0.0.0.0", "--port", "5000", "--workers", "1"]