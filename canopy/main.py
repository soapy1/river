import os
from typing import List
import datetime

from canopy.park import Park


PARK_URL = os.environ.get("PARK_URL")
TARGET_PATH = os.environ.get("TARGET_PATH")


def inspect_park_checkpoints(namespaces: List[str]) -> List[str]:
    """Generate a list of checkpoints for all the environments
    in the given namespace. If latest is True, only the latest
    checkpoint is returned for each environment.
    """
    park_api = Park(url=PARK_URL)
    checkpoints = {}
    for namespace in namespaces:
        envs = park_api.list_environments(namespace=namespace)
        for env in envs:
            checks = park_api.list_checkpoints(
                namespace=namespace, environment=env
            )
            for chk in checks:
                env_chk = park_api.get_checkpoint(namespace, env, chk)
                env_timestamp = datetime.datetime.fromisoformat(env_chk.timestamp)
                save_checkpoint = {
                        "created": env_timestamp,
                        "fqn": f"{namespace}/{env}/{chk}",
                    }

                current_latest_checkpoint = checkpoints.get(f"{namespace}/{env}")
                if current_latest_checkpoint is None:
                    checkpoints[f"{namespace}/{env}"] = {
                        "latest": save_checkpoint,
                        "checkpoints": [save_checkpoint]
                    }
                elif (env_timestamp > current_latest_checkpoint["latest"]["created"]):
                    checkpoints[f"{namespace}/{env}"]["latest"] = save_checkpoint
                else:
                    checkpoints[f"{namespace}/{env}"]["checkpoints"].append(save_checkpoint)

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
    checkpoints = inspect_park_checkpoints(WATCHED_NAMESPACES)
    print(f"checkpoints: {checkpoints}")


if __name__ == "__main__":
    sync()
