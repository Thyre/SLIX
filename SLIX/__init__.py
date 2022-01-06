"""
Scattered Light Imaging ToolboX (SLIX) – an open-source Python package that allows a fully automated evaluation of SLI
measurements and the generation of different parameter maps
"""
__version__ = '2.4.0'
__all__ = ['toolbox', 'io', 'visualization', 'preparation',
           'attributemanager', 'classification']

from . import toolbox, io, visualization, preparation, attributemanager, classification
