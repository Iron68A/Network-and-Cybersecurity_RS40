# -*- coding: utf-8 -*-
"""

Created on May 2022
@author: Mr ABBAS-TURKI

"""

import pem

RESOURCES_DIR = "resources/"
CA_PRIVATE_KEY_FILENAME = RESOURCES_DIR + "ca-private-key.pem"
CA_PUBLIC_KEY_FILENAME = RESOURCES_DIR + "ca-public-key.pem"
SERVER_PRIVATE_KEY_FILENAME = RESOURCES_DIR + "server-private-key.pem"
SERVER_CSR_FILENAME = RESOURCES_DIR + "server-csr.pem"
SERVER_PUBLIC_KEY_FILENAME = RESOURCES_DIR + "server-public-key.pem"


def print_perms(filename: str):
    print(pem.parse_file(filename))