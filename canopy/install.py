import os
import subprocess

from canopy.data_dir import DataDir


def install(target: str, uuid: str, data_dir: DataDir):
    # ensure the target dir exists
    target = os.path.abspath(target)

    # find the checkpoint the user wants to install
    checkpoints = data_dir.get_all_environment_checkpoints()
    checkpoints_flatten = []
    for chk in checkpoints.values():
        checkpoints_flatten += chk
    target_checkpoint = [chk for chk in checkpoints_flatten if chk.uuid == uuid]
    if len(target_checkpoint) == 0:
        print(f"checkpoint {uuid} not found!")
    else:
        # drop the checkpoint spec + lockfile into the target dir
        target_checkpoint = target_checkpoint[0]
        # lockfile = target_checkpoint.environment.lockfile.replace()
        with open(os.path.join(target, "pixi.lock"), "w") as f:
            f.write(target_checkpoint.environment.lockfile)
        with open(os.path.join(target, "pixi.toml"), "w") as f:
            f.write(target_checkpoint.environment.spec)

        print(f"installing target checkpoint for {uuid}")
        p = subprocess.Popen(["pixi", "install"], cwd=target)
        p.wait()
