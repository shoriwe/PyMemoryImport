# adding dependencies to the module zip
import string
from .sub_module import hello_from_sub_module_functions


def hello_init():
    print("Hello!!! From dir_module.__init__")