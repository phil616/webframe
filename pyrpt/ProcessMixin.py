from typing import Union, Optional
from libs.Serializer import Serializer
from pyrpt.RPT import FunctionCodeObject, assemble, disassemble
from functools import wraps,reduce

serializer = Serializer()


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
                 pyversion: Optional[tuple]=None,
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

    def check_prerequisite(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            res = tuple(str(func.__name__).split("_"))
            error_info = "Prerequisite check failed. Check whether the previous steps have been completed"
            if res[0] == "E":
                if not self.E_status.get(res[1]):
                    raise PRTProcedureException(f"{res[0]} process exception when processing [{res[1]}] check failed:"+
                                                error_info)
            else:
                if not self.D_status.get(res[1]):
                    raise PRTProcedureException(f"{res[0]} process exception when processing [{res[1]}] check failed:" +
                                                error_info)
            return func(self, *args, **kwargs)

        return wrapper

    def auto_run(self):
        if self.eprocess:
            self.E_b64decode().E_decrypt().E_decode()
        else:
            self.D_encode().D_encrypt().D_b64encode()


    def get_e(self):
        return self.eprocess

    @check_prerequisite
    def E_b64decode(self):
        self.form = serializer.char_to_bin(self.form)
        self.E_status.update({"decrypt": True})
        return self

    @check_prerequisite
    def E_decrypt(self):
        self.form = serializer.decrypt(self.form, self.exchangeKey)
        self.E_status.update({"decode": True})
        return self

    @check_prerequisite
    def E_decode(self):
        self.form = serializer.bin_to_object(self.form)
        return self

    @check_prerequisite
    def D_encode(self):
        self.form = serializer.obj_to_bin(self.form)
        self.D_status.update({"encrypt": True})
        return self

    @check_prerequisite
    def D_encrypt(self):
        self.form = serializer.encrypt(self.form, self.exchangeKey)
        self.D_status.update({"b64encode": True})
        return self

    @check_prerequisite
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


