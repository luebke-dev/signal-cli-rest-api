FROM python:3.8.3-buster

RUN apt-get update \
    && apt-get install -y --no-install-recommends wget default-jre software-properties-common git locales

# Install Poetry & disable virtualenv creation
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Download & Install signal-cli
RUN cd /tmp/ \
    && git clone https://github.com/AsamK/signal-cli.git \
    && cd signal-cli \
    && ./gradlew build \
    && ./gradlew installDist \
    && ln -s /tmp/signal-cli/build/install/signal-cli/bin/signal-cli /usr/bin/signal-cli


WORKDIR /usr/src/app
# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry install --no-root --no-dev
COPY ./docker-start.sh ./start.sh
RUN chmod +x start.sh
COPY ./signal_cli_rest_api/ signal_cli_rest_api/
EXPOSE 8000
CMD ["bash", "start.sh"]
