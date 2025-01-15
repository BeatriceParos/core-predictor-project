
import sys
from importlib import util
def load_file_as_module(name, location):
    sys.path.insert(0,location.rsplit('/', 1)[0])
    spec = util.spec_from_file_location(name, location)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
sys.argv = [ "/mnt/c/Users/Bea/Desktop/proiectBea/workspace/latest/snipersim/scripts/core_state_predictor.py", "" ]
load_file_as_module("core_state_predictor","/mnt/c/Users/Bea/Desktop/proiectBea/workspace/latest/snipersim/scripts/core_state_predictor.py")

