#!/usr/bin/env python
"""
    Class TuneInput -- contains subroutines to deal with tuning input file
"""    
from os.path import isfile, splitext
import re

class TuneInput:
    def initialize_variables(self):
        self.program = ''
        self.geometry = {}
        self.basis = {}
        self.ecp = {}
        self.charge = 0
        self.dft = []
        self.tune = {}

    # default __init__ function
    def __init__(self):
        self.initialize_variables()

    # call __init__ with a filename, read file and process input
    def __init__(self, filename):
        # First call our base init function to initialize variables
        self.initialize_variables()

        # program will contain the file extension '.tune-nw' or '.tune-g09'
        if splitext(filename)[-1] not in ['.tune-nw', '.tune-g09']:
            raise Exception('FileName Error: file extension should be ".tune-nw" or ".tune-g09"')
        else:
            self.program = splitext(filename)[-1]

        # We will loop through the file using a generator
        #  need access to 'next' function
        with open(filename, 'r') as f:
            f_gen = (x for x in f)
            for i in f_gen:
                # line contains lowercase white space removed string
                # key splits line with space and { character
                line = i.strip().lower()
                key = re.split(' |{', line)

                # Deal with empty lines and commented lines
                if line == '' or line[0] == '#':
                    pass
                
                # charge line
                elif key[0] == 'charge':
                    spl = re.split(' ', line)
                    if len(spl) != 2:
                        raise Exception('Charge Keyword Error: See documentation for charge definition')
                    else:
                        self.charge = spl[-1]

                #  geometry block
                elif key[0] == 'geometry':
                    # use 'next()' to traverse until we find end }
                    self.geometry['geometry'] = []
                    self.geometry['options'] = []
                    line = next(f_gen).strip().lower()
                    while True:
                        spl = line.split()
                        if line == '' or line[0] == '#':
                            line = next(f_gen).strip().lower()
                        elif line[0] == '}':
                            break
                        else:
                            # Check to see if any options are actually specified
                            if spl[0] == 'option' and len(spl) <= 1:
                                raise Exception('Geometry Block Keyword Error: See documentation for "option" keyword')
                            elif spl[0] == 'option': 
                                self.geometry['option'] = spl[1:]
                            else:
                                # Check to see if there is actually an atomic vector here
                                try:
                                    [float(x) for x in spl[1:4]]
                                    self.geometry['geometry'].append(line)
                                except ValueError:
                                    raise Exception('Geometry Block Error: Expected atomic vector on line -- {0}'.format(line))
                            line = next(f_gen).strip()

                #  basis block
                elif key[0] == 'basis':
                    # use 'next()' to traverse until we find end }
                    self.basis['basis'] = []
                    self.basis['option'] = []
                    line = next(f_gen).strip().lower()
                    while True:
                        spl = re.split(' ', line)
                        if line == '':
                            line = next(f_gen).strip()
                        elif line[0] == '}':
                            break
                        else:
                            if spl[0] == 'option' and len(spl) != 2:
                                raise Exception('Basis Block Keyword Error: See documentation for "option" keyword')
                            elif spl[0] == 'option':
                                if spl[1] not in ['global', 'specific', 'generic']:
                                    raise Exception('Basis Block Keyword Error: {0} is not an available option, see documentation'.format(spl[1]))
                                self.basis['option'] = spl[1]
                            else:
                                self.basis['basis'].append(line)
                            line = next(f_gen).strip()

                #  ecp block which we will put in the 
                elif key[0] == 'ecp':
                    # use 'next()' to traverse until we find end }
                    self.ecp['ecp'] = []
                    self.ecp['option'] = []
                    line = next(f_gen).strip().lower()
                    while True:
                        spl = re.split(' ', line)
                        if line == '':
                            line = next(f_gen).strip()
                        elif line[0] == '}':
                            break
                        else:
                            if spl[0] == 'option' and len(spl) != 2:
                                raise Exception('ECP Block Keyword Error: See documentation for "option" keyword')
                            elif spl[0] == 'option':
                                if spl[1] not in ['global', 'specific', 'generic']:
                                    raise Exception('ECP Block Keyword Error: {0} is not an available option, see documentation'.format(spl[1]))
                                self.ecp['option'] = spl[1]
                            else:
                                self.ecp['ecp'].append(line)
                            line = next(f_gen).strip()

                # dft block
                #  Only non standard stuff here, therefore any input check doesn't make sense
                elif key[0] == 'dft':
                    # use 'next()' to traverse until we find end }
                    line = next(f_gen).strip().lower()
                    while True:
                        if line == '' or line[0] == '#':
                            line = next(f_gen).strip()
                        elif line[0] == '}':
                            break
                        else:
                            self.dft.append(line)
                            line = next(f_gen).strip()

                # tune block
                elif key[0] == 'tune':
                    # use 'next()' to traverse until we find end }
                    line = next(f_gen).strip().lower()
                    while True:
                        if line == '' or line[0] == '#':
                            line = next(f_gen).strip()
                        elif line[0] == '}':
                            break
                        else:
                            spl = line.split()
                            if len(spl) != 2:
                                raise Exception('Tune Block Error: this block can only contain key value pairs, see documentation')
                            else:
                                self.tune[spl[0]] = spl[1]
                            line = next(f_gen).strip()

        # Now that we have read our input file, let's run some checks!
        self.run_input_checks()

    def run_input_checks(self):
        '''
        Here we will check options and keywords in basis, ecp, and tune
        '''
        raise NotImplemented('This feature is in the development phase')
