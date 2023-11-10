FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /final_project
# Install dependencies
COPY Pipfile Pipfile.lock /final_project/
RUN pip install pipenv && pipenv install --system
# Copy project
COPY . /final_project/
