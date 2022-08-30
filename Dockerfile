# Set up a base build container and use to install pip dependencies
FROM python:3.10-slim-bullseye as base
FROM base as builder
RUN apt update -y && apt install -y build-essential libpq-dev
RUN pip install pipenv
RUN mkdir /install
WORKDIR /install
COPY Pipfile.lock /install/Pipfile.lock
RUN pipenv requirements >requirements.txt
RUN pip install --ignore-installed --prefix=/install --no-warn-script-location -r requirements.txt

# Copy over pip dependencies from base
FROM base
COPY --from=builder /install /usr/local

# Install libpq package to make psycopg2 work
RUN apt update -y && apt install -y libpq5 && apt clean

# Set up /app as our runtime directory
RUN mkdir /app
WORKDIR /app

# Run as non-root user
RUN useradd -M gunicorn
USER gunicorn

# Add everything except what is in .dockerignore
COPY ./ .

# Run gunicorn as a production-suitable app server
EXPOSE 7777
CMD gunicorn --workers 4 --bind 0.0.0.0:7777 challenge.wsgi --keep-alive 5 --log-level info --access-logfile -
