
class SerializeBaseException(Exception):
    def __init__(self, err_info):
        super().__init__(self)
        self.error_info = err_info

    def __str__(self):
        return self.error_info


class EncryptionError(SerializeBaseException):
    def __init__(self, err_info, encrypt_algorithm):
        super().__init__(err_info)
        self.encrypt_algorithm = encrypt_algorithm

    def __str__(self):
        notice = f"Encryption Error while using {self.encrypt_algorithm}: {self.error_info}"
        return notice
