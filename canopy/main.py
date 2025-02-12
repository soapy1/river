import os
from typing import List

from canopy.park import Park


PARK_URL = os.environ.get("PARK_URL")
TARGET_PATH = os.environ.get("TARGET_PATH")


def inspect_park_checkpoints(namespaces: List[str], latest: bool = True) -> List[str]:
    """Generate a list of checkpoints for all the environments
    in the given namespace. If latest is True, only the latest
    checkpoint is returned for each environment.
    """
    park_api = Park(url=PARK_URL)
    checkpoints = []
    for namespace in namespaces:
        envs = park_api.list_environments(namespace=namespace)
        for env in envs:
            checks = park_api.list_checkpoints(
                namespace=namespace, environment=env
            )
            for chk in checks:
                checkpoints.append(f"{namespace}/{env}/{chk}")

    return checkpoints


def inspect_volume_environments():
    pass


def sync():
    WATCHED_NAMESPACES = os.environ.get("WATCHED_NAMESPACES")
    if WATCHED_NAMESPACES is None:
        WATCHED_NAMESPACES = []
    else:
        WATCHED_NAMESPACES = WATCHED_NAMESPACES.split(",")

    # get checkpoints for all the watched namespaces
    checkpoints = inspect_park_checkpoints(WATCHED_NAMESPACES, latest=True)
    print(f"checkpoints: {checkpoints}")


if __name__ == "__main__":
    sync()
