# Canopy

The goal of this project is to prove out syncing environments from (park)[github.com/soapy1/park] to a volume. 

Canopy will sync environments from park to a given volume, so that the latest checkpoint for an environment is always available.

This can be used by applications like jupyter to provision environments.

## Running

To setup canopy, you'll need to setup some env vars:
* `PARK_URL`: the full URL to the park server
* `TARGET_PATH`: the full path to sync environments to
* `WATCHED_NAMESPACES`: list of namespaces in park to watch for updates, seperated by commas, no spaces. For example, `sophia,dev,everyone`

Run the project with pixi
```
$ pixi install
$ pixi run canopy
```

### Using docker

Build the docker image:

```
$ docker build -t canopy:local .  
```

Run the image (this will sync environments to `./tmp`)
```
$ docker run -it  -v $PWD/tmp:/tmp/canopy  -e PARK_URL=<PARK_URL> -e WATCHED_NAMESPACES=<watchec namespace> canopy:local
```