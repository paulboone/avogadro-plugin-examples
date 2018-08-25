# Avogadro Plugin Examples

DEPRECATED => These examples will not precisely work in Avogadro 2.0; please see examples in Avogadro 2.0 source code.

This repository holds templates you can use to create your own python plugins for avogadro.

At a high-level, a plugin contains:
- information on what it does.
- an install script.
- a script that defines the user interface.
- a script that takes a molecular structure and modifies it in some way!

## Python Plugins

The simplest way to get started is to use the python plugin interface! The python plugin interface requires python 3.5.

A plugin is just a directory with the following files:

- plugin.json: a json file containing information about your plugin and any commands it implements.
- script(s) for each command.
- a [requirements.txt file](https://pip.pypa.io/en/stable/user_guide/#requirements-files) (optional) if your plugin depends on other python modules.

See [bond doubler](./molecule_scaler) for a complete example.

### Plugin.json

The file that defines how your plugin works is the plugin.json. Here is an example plugin.json file that uses the avogadro-plugin template for python:

```
{
  "author": "Paul Boone",
  "version": 0.1,
  "name": "molecule_scaler",
  "url": "https://github.com/paulboone/avogadro-plugin-examples",
  "description": "This is a template plugin you can use as a starting point when designing your own plugins.",
  "commands": [{
      "name": "molecule_scaler",
      "command": "avogadro-plugin-python-run",
      "args": "molecule_scaler"
  }]
}
```

Most of the fields are metadata fields that will be displayed in the avogadro interface.

### commands

This is an array of commands that your plugin supports. A command consists of three fields: name, command and args.

#### name

This is the name of your plugin, as displayed in avogadro.

#### command

This is the command that gets run when this command from your plugin gets invoked. This can either be a command on your PATH or it can be relative to the directory (e.g. "./run.sh").

If you are using the avogadro-plugin python template, this will always be "avogadro-plugin-python-run". The python module name of your actual command script will be setup as an arg below.

#### args

If the command requires additional args prior to the standard args, they are added here.

If you are using the avogadro-plugin python template, this is the name of your python module.

### Command Scripts

A python module command script must implement two methods:

```
def get_dialog_options(structure, params):
...
def run_transformation(structure, params):
```

Both methods are passed the same arguments: structure is the currently selected molecule in avogadro, and params are the user-configured parameters setup by the interface you've defined.

See the molecue_scaler example for a simple and fully-worked out example!

## Shell plugins

The plugin interface is implemented by avogadro making three different calls to scripts in your plugin directory:
1) `install`: for setting up any requirements your plugin needs, or providing instructions on how to do so. Anything output by the script will get displayed by avogadro. Should return 0 for success, or anything else for failure (like a standard shell script).
2) `{your script name} --print-dialog`: avogadro will pass the selected molecule in cjson format to the script's stdin, and the script is expected to return a json structure that contains info on how to setup the user interface.
3) `{your script name} --run-transformation`: avogadro will pass the selected molecule in cjson format along with the user interface settings to the script's stdin. The script is expected to return a new cjson structure file to replace the current molecule.

While it is possible to implement all the command line scripts yourself, we highly recommend using our standard python plugin interface. The python plugin interface takes care of most of the boilerplate for you, including argument processing, stdin handling, json communication, as well as providing a means to install your own python dependencies in an isolated virtual environment. This should be ideal for all but the most unusual / complex plugins!
