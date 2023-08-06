from dataclasses import asdict, dataclass, FrozenInstanceError
from dataclasses import replace as replace_dataclass
from functools import partial
from pathlib import Path

import click

from configobj import ConfigObj


__version__ = "0.0.3"

DEFAULT_FILE = "config.ini"


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
    return obj.from_dict(config_obj, replace=replace)


def from_dict(obj, data, replace=False):
    if not replace:
        for k, v in data.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        return obj
    else:
        fields = {k: v for k, v in data.items() if hasattr(obj, k)}
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


def click_option(obj, *param_decls, **attrs):
    param_decls = param_decls or ("--conf",)

    def wrap(func):
        attrs.setdefault("is_eager", True)
        attrs.setdefault("help", "Read configuration from FILE")
        attrs.setdefault("expose_value", False)
        path = attrs.pop("path", DEFAULT_FILE)
        attrs["callback"] = partial(_file_option_callback, obj, path=path)
        config_update_option = click.option(
            "--config-update",
            is_eager=False,
            expose_value=False,
            hidden=True,
            callback=partial(_config_update_callback, obj),
        )
        return config_update_option(click.option(*param_decls, **attrs)(func))

    return wrap


def _file_option_callback(obj, ctx, option, value, path):
    ctx.default_map = ctx.default_map or {}
    path = value or path
    obj.load(path=value)
    options = asdict(obj)
    ctx.default_map.update(options)


def _config_update_callback(obj, ctx, option, value):
    data = {k: v for k, v in ctx.params.items() if v is not None}
    obj.from_dict(data)


def dataconfig(
    _cls=None,
    *,
    file=DEFAULT_FILE,
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
        setattr(cls, "from_dict", from_dict)
        setattr(cls, "click_option", click_option)
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
