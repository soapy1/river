import os

from canopy.park import Park


def sync():
    PARK_URL = os.environ.get("PARK_URL")
    TARGET_PATH = os.environ.get("TARGET_PATH")
    WATCHED_NAMESPACES = os.environ.get("WATCHED_NAMESPACES")
    if WATCHED_NAMESPACES is None:
        WATCHED_NAMESPACES = []
    else:
        WATCHED_NAMESPACES = WATCHED_NAMESPACES.split(",")


    park_api = Park(url=PARK_URL)
    checkpoints = []
    for namespace in WATCHED_NAMESPACES:
        envs = park_api.list_environments(namespace=namespace)
        for env in envs:
            checks = park_api.list_checkpoints(
                namespace=namespace, environment=env
            )
            for chk in checks:
                checkpoints.append(f"{namespace}/{env}/{chk}")
    
    print(f"checkpoints: {checkpoints}")


if __name__ == "__main__":
    sync()
