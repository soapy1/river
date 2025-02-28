import os
from typing import List
import datetime

from canopy.park import Park
from canopy.data_dir import DataDir


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
                        "checkpoint": env_chk,
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


def save_checkpoints(checkpoints, path):
    data_dir = DataDir(data_dir=path)
    for namespace_env, checkpoint_dict in checkpoints.items():
        latest_uuid = checkpoint_dict["latest"]["checkpoint"].uuid
        # save all the checkpoints
        for checkpoint in checkpoint_dict["checkpoints"]:
            latest = False
            if checkpoint["checkpoint"].uuid == latest_uuid:
                latest = True
            print(f"saving checkpoint {checkpoint['fqn']}! latest: {latest}")

            # HACK: major hacks. clean this up.
            data_dir.save_environment_checkpoint(
                checkpoint=checkpoint["checkpoint"],
                namespace=namespace_env.split("/")[0],
                env=namespace_env.split("/")[1],
                latest=latest,
            ) 

def sync():
    WATCHED_NAMESPACES = os.environ.get("WATCHED_NAMESPACES")
    if WATCHED_NAMESPACES is None:
        WATCHED_NAMESPACES = []
    else:
        WATCHED_NAMESPACES = WATCHED_NAMESPACES.split(",")

    # get path that canopy writes to
    canopy_path = os.environ.get("TARGET_PATH")
    if canopy_path is None:
        canopy_path = "/tmp/canopy"

    # checkpoints get saved to the `checkpoint` dir inside the canopy_path
    target_path = f"{canopy_path}/checkpoints"

    # get checkpoints for all the watched namespaces
    checkpoints = inspect_park_checkpoints(WATCHED_NAMESPACES)
    save_checkpoints(checkpoints, target_path)


if __name__ == "__main__":
    sync()
