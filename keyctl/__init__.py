
# -*- coding: utf-8 -*-

from .keyctlwrapper import KeyctlWrapper
from .keyctlwrapper import KeyNotExistError, KeyAlreadyExistError, KeyctlOperationError

from .key import Key


# -------------------------------------------------------------------


import subprocess

# test for keyctl
try:
    subprocess.check_output(['which', 'keyctl'])
except subprocess.CalledProcessError:
    raise OSError(
        'The commandline util \'keyctl\' must be installed to use this module. ' +
        'Install it via \'apt-get install keyutils\'.'
    )
