# Use an official Python runtime as a parent image
FROM python:3.10-rc-buster as BUILDER
LABEL maintainer="admin@moe.ph"

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV ENV PROD

RUN apt-get update && apt-get install -y --no-install-recommends -y gcc zlib1g-dev libjpeg-dev libjpeg62-turbo libpq-dev postgresql-common libev-dev && pip3 install wheel;

# Setup venv
RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

FROM python:3.10-rc-slim-buster as IMAGE

COPY --from=BUILDER /opt/venv /opt/venv

RUN apt-get update && apt-get install -y --no-install-recommends zlib1g-dev libjpeg-dev libjpeg62-turbo libpq-dev postgresql-common libev-dev libopenjp2-7 libtiff5 libxcb1 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app/
COPY . /app/
# Set the working directory to /app/
WORKDIR /app/

ENV PATH="/opt/venv/bin:$PATH"

RUN useradd blog
RUN chown -R blog /app
USER blog

EXPOSE 8000
CMD exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4
