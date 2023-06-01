FROM python:3.10.8-slim-bullseye as common_runtime

ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=1

### Poetry

ENV POETRY_HOME=/opt/poetry
ENV PATH ${POETRY_HOME}/bin:$PATH
# renovate: datasource=pypi depName=poetry
ENV POETRY_VERSION="1.5.0"

COPY scripts/install-poetry.py /install-poetry.py
# install poetry
RUN python3 install-poetry.py --version ${POETRY_VERSION}

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    curl \
    libjpeg-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./poetry.lock /website/
WORKDIR /website
RUN poetry config virtualenvs.in-project true &&\
  poetry install --only main --no-cache --no-interaction


##############################
## Frontend build container ##
##############################

FROM common_runtime as frontend

WORKDIR /website

ENV NODE_VERSION="18.16.0"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# Install packages
RUN curl -sL https://deb.nodesource.com/setup_18.x | /bin/bash - \
    && apt-get update \
    && apt-cache madison nodejs \
    && apt-get install --no-install-recommends -y \
        nodejs=${NODE_VERSION}-deb-1nodesource1 \
    && rm -rf /var/lib/apt/lists/*

COPY package.json package-lock.json /website/
COPY frontend /website/frontend

# Install and build npm packages
ENV NPM_VERSION="9.6.7"

RUN npm install -g npm@${NPM_VERSION} \
    && npm ci

COPY tailwind.config.js postcss.config.js manage.py  /website/
COPY website /website/website
RUN npm run build
RUN poetry run python manage.py collectstatic -i "*.scss" -i "*.md" -i "*.orig" --no-input

FROM common_runtime as backend

COPY ./ /website/
WORKDIR /website

# Add static files
COPY --from=frontend /website/static /website/static

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD [ "/entrypoint.sh" ]
