# -*- coding: utf-8 -*-
"""

Created on May 2022
@author: Mr ABBAS-TURKI

"""
from tools.core import Configuration, generate_private_key, generate_csr

class Server:

    def __init__(self, config: Configuration, password: str, private_key_filename: str, csr_filename: str):
        self._config = config
        self._private_key = generate_private_key(private_key_filename, password)
        self._csr = generate_csr(self._private_key,csr_filename,config)
        self._private_key_filename = private_key_filename
        self._csr_filename = csr_filename
        self._password = password

    def get_csr(self):
        return self._csr
