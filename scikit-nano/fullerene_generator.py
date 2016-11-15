
from avogadro_plugin.utils import extrapolate_bonds
from sknano.generators import FullereneGenerator

def run_transformation(structure, params):
    """
    This method performs a transformation on the currently selected structure in avogadro, using
    any passed dialog parameters as needed.

    returns a tuple of (status, results) where status = 0 for success, 64 for failure, and the
    results equal a dictionary of the terms to be returned across stdout.
    """

    fg = FullereneGenerator(N=params['N'])

    structure["atoms"]["elements"]["number"] =  [ a.Z for a in fg.atoms ]
    structure["atoms"]["coords"]["3d"] = [ c for a in fg.atoms for c in (a.x, a.y, a.z) ]
    atoms = [ (a.x, a.y, a.z, a.Z) for a in fg.atoms ]
    structure["bonds"]["connections"]["index"] = extrapolate_bonds(atoms)

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
        'name': 'N',
        'type': 'integer',
        'default': 20,
        'minimum': 20,
        'maximum': 100,
    }]
    return options
