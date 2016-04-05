'''
distill: Main module

Copyright 2016, The Charles Stark Draper Laboratory
Licensed under Apache Software License.
'''

from __future__ import absolute_import

import sys
if sys.version_info[:2] < (2, 7):
    m = "Python 2.7 or later is required for Distill (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys


def main():
    '''
    Main function of the boilerplate code is the entry point of the 'distill' executable script (defined in setup.py).
    
    Use doctests, those are very helpful.
    
    >>> main()
    Hello World!
    >>> 2 + 2
    4
    '''
    
    print("Hello World!")

