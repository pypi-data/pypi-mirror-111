from dataclasses import asdict, dataclass, FrozenInstanceError
from dataclasses import replace as replace_dataclass
from pathlib import Path

from configobj import ConfigObj


__version__ = "0.0.2"


def locate(file, paths, auto, file_path=""):
    if file_path:
        return Path(file_path)
    elif auto:
        for _path in paths:
            path = Path(_path).joinpath(file)
            if path.exists():
                return path
        return Path(".").joinpath(file)
    else:
        raise FileNotFoundError(f"File {file!r} not found at {paths}.")


def load(obj, path="", unrepr=True, replace=False):
    path = locate(
        file=obj._file, paths=obj._paths, auto=obj._auto, file_path=path
    )
    config_obj = ConfigObj(str(path), unrepr=unrepr)
    if not replace:
        for k, v in config_obj.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        return obj
    else:
        fields = {k: v for k, v in config_obj.items() if hasattr(obj, k)}
        return replace_dataclass(obj, **fields)


def save(obj, path="", unrepr=True, overwrite=False):
    path = locate(
        file=obj._file, paths=obj._paths, auto=obj._auto, file_path=path
    )
    config_obj = ConfigObj(unrepr=unrepr)
    config_obj.update(asdict(obj))
    if path.exists() and not overwrite:
        raise FileExistsError(f"File {path} exists, refusing to overwrite.")
    with path.open("wb") as outfile:
        config_obj.write(outfile)
    return obj

def dataconfig(
    _cls=None,
    *,
    file="config.ini",
    paths=None,
    auto=True,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
):
    def wrap(cls):
        setattr(cls, "_file", file)
        setattr(cls, "_paths", paths or ["."])
        setattr(cls, "_auto", auto)
        setattr(cls, "load", load)
        setattr(cls, "save", save)
        wrapped_cls = dataclass(
            cls,
            init=init,
            repr=repr,
            eq=eq,
            order=order,
            unsafe_hash=unsafe_hash,
            frozen=frozen,
        )
        return wrapped_cls

    if _cls is None:
        return wrap

    return wrap(_cls)
