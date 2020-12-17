FROM python:3.8-alpine

RUN apk add --no-cache openjdk11-jre

# Download & Install signal-cli
ENV SIGNAL_CLI_VERSION=0.7.0
RUN cd /tmp/ \
    && wget https://github.com/AsamK/signal-cli/releases/download/v"${SIGNAL_CLI_VERSION}"/signal-cli-"${SIGNAL_CLI_VERSION}".tar.gz \
    && tar xf signal-cli-"${SIGNAL_CLI_VERSION}".tar.gz -C /opt \
    && ln -s /opt/signal-cli-"${SIGNAL_CLI_VERSION}"/bin/signal-cli /usr/bin/si\
gnal-cli

WORKDIR /usr/src/app
# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* ./

# Install Poetry & disable virtualenv creation
RUN wget -q -O - https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
    
RUN apk add --no-cache --virtual build-dependencies gcc make musl-dev && poetry install --no-root --no-dev && apk del build-dependencies

COPY ./docker-start.sh ./start.sh
RUN chmod +x start.sh
COPY ./signal_cli_rest_api/ signal_cli_rest_api/

EXPOSE 8000
CMD ["./start.sh"]
