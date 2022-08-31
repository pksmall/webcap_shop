# Python version
FROM python:3.9
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install gettext to compile tranlations
RUN apt-get update && apt-get install gettext -y

# Install pipenv
RUN pip install --upgrade pip

# Copy requirements.txt
COPY requirements.txt /code

# Install requirements
RUN pip install -r requirements.txt
