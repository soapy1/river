import os
from typing import List
import datetime
import yaml

from canopy.park import Park


PARK_URL = os.environ.get("PARK_URL")


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
                        "checkpoint": chk
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


def save_checkpoin_to_volume(checkpoints, path):
    park_api = Park(url=PARK_URL)

    checkpoint_files_path = f"{path}/checkpoints/"
    os.makedirs(checkpoint_files_path, exist_ok=True)
    for namespace_env, checkpoint_dict in checkpoints.items():
        latest_checkpoint = checkpoint_dict["latest"]["checkpoint"]
        print(f"latest checkpoint for {namespace_env} is {latest_checkpoint}")
        checkpoint_file = f"{checkpoint_files_path}/{namespace_env}/{latest_checkpoint}"
        # see if latest checkpoint already exists
        if os.path.exists(checkpoint_file):
            print(f"checkpoint file already exists at {checkpoint_file}, skipping")
        else:
            os.makedirs(f"{checkpoint_files_path}/{namespace_env}", exist_ok=True)
            latest_checkpoint = park_api.get_checkpoint(namespace_env.split("/")[0], namespace_env.split("/")[1], latest_checkpoint)
            with open(checkpoint_file, "w+") as file:
                yaml.dump(latest_checkpoint.model_dump(), file)


def sync():
    WATCHED_NAMESPACES = os.environ.get("WATCHED_NAMESPACES")
    if WATCHED_NAMESPACES is None:
        WATCHED_NAMESPACES = []
    else:
        WATCHED_NAMESPACES = WATCHED_NAMESPACES.split(",")

    target_path = os.environ.get("TARGET_PATH")
    if target_path is None:
        target_path = "/tmp/canopy"

    # get checkpoints for all the watched namespaces
    checkpoints = inspect_park_checkpoints(WATCHED_NAMESPACES)
    print(f"checkpoints: {checkpoints}")
    save_checkpoin_to_volume(checkpoints, target_path)


if __name__ == "__main__":
    sync()
