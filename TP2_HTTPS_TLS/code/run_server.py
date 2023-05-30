# -*- coding: utf-8 -*-
"""

Created on May 2022
@author: Mr ABBAS-TURKI

"""

from flask import Flask, render_template, request
import hashlib


# définir le message secret
SECRET_MESSAGE = "MDPnul" # A modifier #fait1
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the form data
        id = request.form['id']
        password = request.form['password']
        password = salt +password
        password = hash_password(password)
        # Validate the login credentials
        if id == 'admin' and password == hashsalt:
            # Successful login, redirect to the home page
            return render_template('home.html', id=id, message= SECRET_MESSAGE)
        else:
            # Invalid credentials, show an error message
            error = 'Invalid login credentials. Please try again.'
            return render_template('login.html', error=error)
    else:
        # Show the login form
        return render_template('login.html')

def hash_password(password): 
    #Hasher le mot de passe avec SHA-256 25x
    for i in range(25):
        password = hashlib.sha256(password.encode()).hexdigest()
    return password  

#definir le mot de passe et le hash
password = "pass"
salt = "salt" 
password = salt+password
hashsalt = hash_password(password)


if __name__ == "__main__":
    # HTTP version
    #app.run(debug=True, host="0.0.0.0", port=8081)
    # HTTPS version
    # A compléter  : nécessité de déplacer les bons fichiers vers ce répertoire
    context = ("server-public-key.pem", "server-private-key.pem")
    app.run(debug=True, host="0.0.0.0", port=8081, ssl_context=context)
