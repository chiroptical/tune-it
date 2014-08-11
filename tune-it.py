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
from tune_input import TuneInput


# Begin our script
try:
    # docopt parses command line options via doc string above
    arguments = docopt(__doc__, version='tune-it.py version 0.0.1')
    
    # Read input file and process jobs
    tune = TuneInput(arguments['--input'])

# Exceptions we may want to handle
except (KeyboardInterrupt,SystemExit):
    print('Interrupt Detected! exiting...')

except Exception as e:
    print(e)
