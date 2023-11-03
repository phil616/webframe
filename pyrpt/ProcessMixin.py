from typing import Union, Optional
from libs.Serializer import Serializer
from functools import wraps, reduce
from copy import deepcopy
from types import FunctionType, CodeType
from pydantic import BaseModel
from sys import version_info

serializer = Serializer()

class FunctionCodeObject(BaseModel):
    py_version: tuple = (version_info.major, version_info.minor)
    func_params: list = []
    argcount: int = 0
    posonlyargcount: int = 0
    kwonlyargcount: int = 0
    nlocals: int = 0
    stacksize: int = 0
    flags: int = 0
    codestring: bytes = b''
    constants: tuple = ()
    names: tuple = ()
    varnames: tuple = ()
    filename: str = ''
    name: str = ''
    firstlineno: int = 0
    lnotab: bytes = b''
    freevars: tuple = ()
    cellvars: tuple = ()


def assemble(func, param: list):
    code_object = deepcopy(func.__code__)
    return FunctionCodeObject(**{
        "func_params": param,
        "argcount": code_object.co_argcount,
        "codestring": code_object.co_code,  # codestring and code are different with var names
        "cellvars": code_object.co_cellvars,
        "constants": code_object.co_consts,  # constants and consts are different with var names
        "filename": code_object.co_filename,
        "firstlineno": code_object.co_firstlineno,
        "flags": code_object.co_flags,
        "freevars": code_object.co_freevars,
        "posonlyargcount": code_object.co_posonlyargcount,
        "kwonlyargcount": code_object.co_kwonlyargcount,
        "lnotab": code_object.co_lnotab,
        "name": code_object.co_name,
        "names": code_object.co_names,
        "nlocals": code_object.co_nlocals,
        "stacksize": code_object.co_stacksize,
        "varnames": code_object.co_varnames,
    })


def disassemble(obj: FunctionCodeObject):
    return FunctionType(CodeType(
        obj.argcount,
        obj.posonlyargcount,
        obj.kwonlyargcount,
        obj.nlocals,
        obj.stacksize,
        obj.flags,
        obj.codestring,
        obj.constants,
        obj.names,
        obj.varnames,
        obj.filename,
        obj.name,
        obj.firstlineno,
        obj.lnotab,
        obj.freevars,
        obj.cellvars,
    ), globals())


def exec_object(obj: FunctionCodeObject):
    return disassemble(obj)(*obj.func_params)


class PRTProcedureException(Exception):
    def __init__(self, error):
        self.info = error

    def __str__(self):
        return repr(self.info)


class PRTProcedure(object):
    """
    according to the map
    the form of receive should be base64 encoded,
    [BASE64] ---b64decode---> [BIN(encrypted)] ---decrypt---> [BIN(original)]  ---decode--->  [FunctionCodeObject]  <E>
    [BASE64] <--b64encode---  [BIN(encrypted)] <--encrypt---- [BIN(original)]  <--encode----      ]                 <D>
    """

    def __init__(self,
                 form: Union[FunctionCodeObject, str],
                 pyversion: Optional[tuple] = None,
                 exchangeKey: bytes = None
                 ):
        self.exchangeKey = exchangeKey
        self.pyversion = pyversion
        self.eprocess = None
        self.E_status = {
            "b64decode": False,
            "decrypt": False,
            "decode": False
        }
        self.D_status = {
            "encode": False,
            "encrypt": False,
            "b64encode": False
        }
        if isinstance(form, FunctionCodeObject):
            self.eprocess = False
        if isinstance(form, str):
            self.eprocess = True

        self.E_status.update({"b64decode": True})
        self.D_status.update({"encode": True})
        self.form = form

    def auto_run(self):
        if self.eprocess:
            self.E_b64decode().E_decrypt().E_decode()
        else:
            self.D_encode().D_encrypt().D_b64encode()

    def get_e(self):
        return self.eprocess


    def E_b64decode(self):
        self.form = serializer.char_to_bin(self.form)
        self.E_status.update({"decrypt": True})
        return self


    def E_decrypt(self):
        self.form = serializer.decrypt(self.form, self.exchangeKey)
        self.E_status.update({"decode": True})
        return self


    def E_decode(self):
        self.form = serializer.bin_to_object(self.form)
        return self


    def D_encode(self):
        self.form = serializer.obj_to_bin(self.form)
        self.D_status.update({"encrypt": True})
        return self


    def D_encrypt(self):
        self.form = serializer.encrypt(self.form, self.exchangeKey)
        self.D_status.update({"b64encode": True})
        return self


    def D_b64encode(self):
        self.form = serializer.bin_to_char(self.form)
        return self

    @property
    def FunctionObject(self):
        if not reduce(lambda x, y: x and y, self.E_status.values(), True):
            raise PRTProcedureException("Process has not completed")
        return self.form

    @property
    def b64string(self):
        if not reduce(lambda x, y: x and y, self.D_status.values(), True):
            raise PRTProcedureException("Process has not completed")
        return self.form
