# zycelium.dataconfig

Create [dataclasses](https://docs.python.org/3/library/dataclasses.html) backed by configuration files.

[![Python package](https://github.com/zycelium/dataconfig/actions/workflows/python-package.yml/badge.svg)](https://github.com/zycelium/dataconfig/actions/workflows/python-package.yml)

## Usage

### Use defaults:

Create a new python script and name it `example.py`

```python
from zycelium.dataconfig import dataconfig


@dataconfig
class Config:
    name: str = "World"

config = Config().load()

print(f"Hello, {config.name}!")
```

Create a `config.ini` file in the same directory as `example.py`

```ini
name = "DataConfig"
```

Finally, from the same directory, run `python example.py` , 
your console session should look something like this:

```console
$ python example.py
Hello, DataConfig!
```

The defaults here are:

- Config file name: `"config.ini"`
- Paths to look for the config file (current working directory): `["."]`

### Specify file-name for configuration:

```python
from zycelium.dataconfig import dataconfig


@dataconfig(file="custom_config.ini")
class Config:
    name: str = "World"

config = Config().load()

print(f"Hello, {config.name}!")
```

In this example, we specify the file-name on this line:
`@dataconfig(file="custom_config.ini")` with keyword arguments
`file="custom_config.ini"` passed to `@dataconfig()`.

### Specify file-lookup-paths:

```python
from zycelium.dataconfig import dataconfig


@dataconfig(paths=[".", "examples", "/usr/local/etc"])
class Config:
    name: str = "World"

config = Config().load()

print(f"Hello, {config.name}!")
```

Here, we pass `paths=[".", "examples"]` to `@dataconfig()`
to specify the paths on filesystem where `dataconfig` should
look for the default `"config.ini"` file. We can also specify
the filename along with the paths. Paths can be relative 
to current working directory or absolute.

### Save configuration to file:

```python
from zycelium.dataconfig import dataconfig

FILE_NAME = "newconfig.ini"

@dataconfig(file=FILE_NAME)
class Config:
    name: str = "World"

config = Config()
config.save()

print(f"Saved config to file: {FILE_NAME}.")
```

Here, we set the config-file-name while creating the class,
when `save()` is called, it will create the file and save
contents of `Config`.

If we try running the same example again, we will get an error:

`FileExistsError: File newconfig.ini exists, refusing to overwrite.`

This is to protect us from accidentally overwriting an existing config file.
To overwrite it, pass `overwrite=True` to `save()` like this:

`config.save(overwrite=True)`

### Frozen configuration:

```python
from zycelium.dataconfig import dataconfig


@dataconfig(frozen=True)
class Config:
    name: str = "World"

config = Config().load(replace=True)

print(f"Hello, {config.name}!")
```

To load a frozen config, we need to pass `replace=True` to `load()`,
if we forget, we get the error:

`dataclasses.FrozenInstanceError: cannot assign to field 'name'`

Once loaded, we cannot overwrite the configuration.


### Use with Click Integration for CLI apps:

Here, dataconfig will generate options for click CLI framework,
one to add defaults to all options with names that exist in
the dataconfig class, overridden by values found in the configuration
file. These options can be overridden by passing values as usual
to the command line.

There's also a new option added to the command: "--conf", which
can be used to specify a different configuration file to load
defaults.

And finally, any changes made in the command line are applied to
the dataconfig object, but not saved to the configuration file
unless the `save()` method is called later.

Frozen dataconfig does not work with commandline integration.

```python
import click
from zycelium.dataconfig import dataconfig


@dataconfig
class Config:
    name: str = "World"


config = Config()
# No need to load() config when using click_option()


@click.command()
@click.option("--name")
@config.click_option()
def main(name):
    print(f"Hello, {name}!")
    print(f"Hello, {config.name}!")


main()
```


### For more examples:

Read through the `tests/` directory, where you will find the 
expected usage and how and why dataconfig can fail.


## Install

From [PyPI](https://pypi.org/)

```console

pip install zycelium.dataconfig
```

From source:

```console

git clone https://github.com/zycelium/dataconfig.git
cd dataconfig
pip install -e .
```
