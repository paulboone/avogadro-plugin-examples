#!/usr/bin/env python3
# This is a test script for testing whether the plugin's interface was created to spec.
# To use:
# - make sure the install script has been run in the plugin directory
#   e.g. for a python plugin, run avogadro-plugin-python-install
# - cd to the plugin dir
# - run: ${path to test.py} < ${path to molecule.json file}
#   e.g. ../test.py < ../support/ethane.json

import json
import subprocess
from subprocess import PIPE, STDOUT, Popen
import sys

with open("./plugin.json") as f:
    plugin_json = json.load(f)

molecule_json = json.load(sys.stdin)

for command in plugin_json['commands']:

    full_cmd = "%s %s --print-dialog" % (command['command'], command['args'])
    print("\n\n%s: " % full_cmd)
    proc = subprocess.Popen([full_cmd], shell=True, stdin=PIPE, stdout=PIPE, universal_newlines=True)
    stdout, stderr = proc.communicate(input=json.dumps(molecule_json))
    results_json = json.loads(stdout)
    print(results_json)

    options = { opt['name']:opt['default'] for opt in results_json }
    molecule_json['options'] = options

    full_cmd = "%s %s --run-transformation" % (command['command'], command['args'])
    print("\n\n%s: " % full_cmd)
    proc = subprocess.Popen([full_cmd], shell=True, stdin=PIPE, universal_newlines=True)
    proc.communicate(input=json.dumps(molecule_json))

print("\n")
