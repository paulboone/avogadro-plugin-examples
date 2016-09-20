#!/usr/bin/env python3

import json
import sys

import click

def run_transformation(structure, params):
    """
    This method performs a transformation on the currently selected structure in avoagadro, using
    any passed dialog parameters as needed.

    returns a tuple of (status, results) where status = 0 for success, 64 for failure, and the
    results equal a dictionary of the terms to be returned across stdout.
    """

    # As an example, we perform a simple (and pointless) reflect and scale operation here.
    scale = params['Scale']
    for i, coord in enumerate(structure['atoms']['coords']['3d']):
        structure['atoms']['coords']['3d'][i] = -1 * scale * coord

    # put together result information
    # note that you can return a message for display, if there was a result to report or an error.
    results = {
        'message_type': None,
        'message': None,
        'cjson': structure,
    }

    status = 0 # success!
    # status = 64 # fail :(

    return (status, results)


def get_dialog_options(structure, params):
    """
    This method returns a dictionary containing the option information for anything you want
    displayed in the dialog. See docs at @TODO.

    A dictionary of the current selected structure, as well as any existing dialog parameters
    are passed in case your dialog options are context-dependent.
    """
    options = {
        'Scale': {
            'type': 'integer',
            'default': 1,
            'minimum': 1,
            'maximum': 5,
        }
    }
    return options


@click.command()
@click.option('--print-dialog/--run-transformation', default=False)
@click.option('--language', default='en.us', help="preferred language to use")
def run(print_dialog, language):
    """
    This command expects to recieve a JSON file via stdin that contains the structure selected in
    avogadro, along with any parameters from the dialog. You can call this method without flags, in
    which case it will attempt to run the transformation, or with the flag --print-dialog, which
    instead returns the JSON necessary via stdout to create a dialog to set the parameters of the
    transformation.

    A note to people using this as a template:

    This method handles the comand line interface, unmarshals the data from JSON, and passes the
    data to either get_dialog_options() or run_transformation(), depending on the flags. Upon
    completion, it marshals the results back to JSON and returns it to avogadro via stdout.

    In general, you shouldn't need to modify this method. Instead, make changes to
    get_dialog_options() and run_transformation().
    """
    input_stream = click.get_text_stream('stdin').read()
    input_json = json.loads(input_stream)
    structure = input_json['cjson']
    options = input_json['options']

    status = 0
    if print_dialog:
        results = get_dialog_options(structure, options)
    else:
        status, results = run_transformation(structure, options)

    # marshal to json and return across stdout
    sys.stdout.write(json.dumps(results))

    if status:
        sys.exit(status)

if __name__ == '__main__':
    run()
