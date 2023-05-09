# -*- coding: utf-8 -*-
"""

Created on May 2022
@author: Mr ABBAS-TURKI

"""

from flask import Flask

# définir le message secret
SECRET_MESSAGE = "hypsilophodon" # A modifier
app = Flask(__name__)


@app.route("/")
def get_secret_message():
    return SECRET_MESSAGE


if __name__ == "__main__":
    # HTTP version
    app.run(debug=True, host="0.0.0.0", port=8081)
    # HTTPS version
    # A compléter  : nécessité de déplacer les bons fichiers vers ce répertoire
   
