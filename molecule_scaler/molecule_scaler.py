
from avogadro_plugin import avogadro_plugin_call

def run_transformation(structure, options):
    """
    This method performs a transformation on the currently selected structure in avoagadro, using
    any passed dialog parameters as needed.

    returns a tuple of (status, results) where status = 0 for success, 64 for failure, and the
    results equal a dictionary of the terms to be returned across stdout.
    """

    # As an example, we perform a simple scale operation here.
    scale = options['scale']
    for i, coord in enumerate(structure['atoms']['coords']['3d']):
        structure['atoms']['coords']['3d'][i] = scale * coord

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
    options = [{
        'key': 'scale',
        'label': 'Scale',
        'tooltip': 'Multiplier to scale all positions by',
        'type': 'integer',
        'default': 1,
        'minimum': 1,
        'maximum': 5,
    }]
    return options

avogadro_plugin_call(
    method_name="Molecular Scaler",
    run_workflow_method=run_transformation,
    print_options_method=get_dialog_options,
    menu_path="&extensions"
)
