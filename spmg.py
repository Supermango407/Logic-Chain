import sys
import os

external_module_dir = os.path.abspath('../SPMG/')
if external_module_dir not in sys.path:
    sys.path.append(external_module_dir)

from spmg_tkinter.rearrangeable import Rearrangeable