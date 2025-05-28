# Node deps
FROM node:23.9-slim AS bep-vite
WORKDIR /app

RUN npm upgrade -g npm \
    && npm upgrade -g yarn \
    && rm -rf /var/lib/apt/lists/*

# build js deps
COPY bep_vite/package.json bep_vite/yarn.lock /app/
RUN yarn

# run vite build
COPY bep_vite /app
RUN yarn build

FROM bep-vite AS bep-vite-prod
RUN yarn --production \
    && yarn cache clean

# Django app
FROM python:3.13-alpine AS bep
EXPOSE 80
WORKDIR /app

# add system deps
RUN apk update \
    && apk add git libmagic curl gdal geos \
    && pip install --no-cache-dir --upgrade pip \
    && rm -rf /var/cache/apk/*

# install python deps
COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

# add project files
COPY . /app

# add prod assets
COPY --from=bep-vite-prod /app/dist /static-vite/dist
COPY --from=bep-vite-prod /app/node_modules /app/node_modules

# collect static assets for production
RUN python manage.py collectstatic --noinput

# run migrations and start server
CMD ["docker/docker-entrypoint.sh"]