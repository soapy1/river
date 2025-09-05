# River

The goal of this project is to prove out syncing environments from (park)[github.com/soapy1/park] to a volume. 

River will sync environments from park to a given volume, so that the latest checkpoint for an environment is always available.

This can be used by applications like jupyter to provision environments.

## Running

To setup River, you'll need to setup some env vars:
* `PARK_URL`: the full URL to the park server
* `TARGET_PATH`: the full path to sync environments to
* `WATCHED_NAMESPACES`: list of namespaces in park to watch for updates, seperated by commas, no spaces. For example, `sophia,dev,everyone`

Run the project with pixi
```
$ pixi install
$ pixi run River
```

### Using docker

Build the docker image:

```
$ docker build -t River:local .  
```

Run the image (this will sync environments to `./tmp`)
```
$ docker run -it  -v $PWD/tmp:/tmp/River  -e PARK_URL=<PARK_URL> -e WATCHED_NAMESPACES=<watchec namespace> River:local
```

### In Kubernetes

River can be run as a cron job in kubernetes. Note, that you may need to update some config vars in the `containers` section of the cron job yaml file. In particular, `PARK_URL` and `WATCHED_NAMESPACES`.

```
$ kubectl apply -f k8/cronjob.yaml -n <namespace>
```

To see the logs
```
# list past jobs
$ kubectl get jobs -n <namespace>
NAME              COMPLETIONS   DURATION   AGE
River-29011459   1/1           23s        2m9s
River-29011460   1/1           3s         69s
River-29011461   1/1           3s         9s

# get logs for specific job
$ kubectl logs jobs/River-29011459 -n dev-test
saving checkpoint fod-demo/pixi-py/318fd971! latest: True
saving checkpoint fod-demo/pixi-py/e8ed81a9! latest: False
```

#### Debugging with the debug-pod deployment

If you are trying to debug River in kubernetes, you can use the `k8/debug-pod.yaml` deployment.

Apply the deployemnt
```
$ kubectl apply -f k8/debug-pod.yaml -n <namespace>
```

Exec into the pod
```
$ kub exec -it River-76b7d65fc9-9769x -n dev-test -- /bin/bash 
```

The conda shared environment shared volume will be mounted to `/environments`. Double check with the River cron job definition to see where the sync path is. It'll probably be `/environments/data/River/checkpoints`.
