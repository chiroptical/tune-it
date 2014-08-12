#!/usr/bin/env python
""" tune-it.py -- A tuning script
Usage:
    tune-it.py [options]
        (-i <input.tune> | --input <input.tune>)

Positional Arguments:
    -i, --input <input.tune>    A tuning input file for NWChem (input.tune-nw)
                                    or Gaussian (input.tune-g09)

Options:
    -h, --help                  Print this screen and exit
    -v, --version               Print the version of tune-it.py
"""


# Imports
from docopt import docopt
from sys import exit
from os.path import isfile, splitext
from Tune import Tune


# Begin our script
try:
    # docopt parses command line options via doc string above
    arguments = docopt(__doc__, version='tune-it.py version 0.0.1')
    
    # Read input file
    if not isfile(arguments['--input']) or splitext(arguments['--input'])[-1] not in ['.tune-nw', '.tune-g09']:
        raise Exception(('Input Error: {} doesn\'t exist or doesn\'t have the ' +
                         'expected extension, try -h/--help').format(arguments['--input']))
    tune = Tune(arguments['--input'])

    # What step do we need to complete


# Exceptions we may want to handle
except KeyboardInterrupt:
    print('Interrupt Detected! exiting...')

except Exception as e:
    print(e)
