# ref: 
# https://github.com/prefix-dev/pixi-docker
# https://github.com/pavelzw/pixi-docker-example

FROM ghcr.io/prefix-dev/pixi:0.40.2

COPY ./canopy /app/canopy
COPY ./pixi.lock /app/pixi.lock
COPY ./pyproject.toml /app/pyproject.toml

WORKDIR /app
RUN pixi install
CMD ["pixi", "run", "canopy"]