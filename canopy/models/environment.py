# copied from https://github.com/soapy1/fod
# in the future, we can import the fod package

from pydantic import BaseModel


class EnvironmentSpec(BaseModel):
    """Specifies a locked environment from pixi

    spec : str
      The pixi.toml for the environemnt
    
    lockifle : str
      The pixi.lock for the environment

    lockfile_hash : str
      Hash for the content of the lockfile. If the lockfile hash has
      changed, then the environment has been updated. If the spec
      file has changed, it will cause a change in the lockfile as
      well.
    """
    spec: str
    lockfile: str
    lockfile_hash: str


class EnvironmentCheckpoint(BaseModel):
    """An environment at a point in time
    
    Only applys to a particular environment spec
    """
    environment: EnvironmentSpec
    timestamp: str
    # TODO: how do you actually create a uuid?
    uuid: str
    tags: list[str]