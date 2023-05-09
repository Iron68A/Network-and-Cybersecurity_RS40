# -*- coding: utf-8 -*-
"""

Created on Sun May 10 17:08:59 2020
@author: Mr ABBAS-TURKI

Modified on April 2021
@author: Mr Perronnet

"""

# Librairies requises pour générer les clés
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Librairies requises pour la création du certificat de l'autorité de certification
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes


# Classe de définition d'une configuration
class Configuration:

    def __init__(self, country: str, state: str, locality: str, org: str, hostname: str, alt_names = []):
        """
        :param country:
        :param state:
        :param locality:
        :param org:
        :param hostname:
        :param alt_names: alternatives de serveurs DNS valides pour le certificat
        """
        self.country = country
        self.state = state
        self.locality = locality
        self.org = org
        self.hostname = hostname
        self.alt_names = alt_names


# Lecture des paramètres de certification
def read_configuration(config: Configuration):
    return x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, config.country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, config.state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, config.locality),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, config.org),
            x509.NameAttribute(NameOID.COMMON_NAME, config.hostname)
        ]
    )


# Génération clé privée
def generate_private_key(filename: str, password: str):
    # 65537 est l'exposant public magique
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    # Paramètres d'encodage pour le chiffrement de la clé privée
    utf8_pass = password.encode("utf-8")
    algorithm = serialization.BestAvailableEncryption(utf8_pass)

    # Création du fichier "filename" contenant le clés privés (p,q,n) chiffrées avec le "password"
    with open(filename, "wb") as keyfile:
        keyfile.write(
            private_key.private_bytes(
                # FIXME Expected type 'Encoding', got 'str' instead
                encoding=serialization.Encoding.PEM,
                # FIXME Expected type 'PrivateFormat', got 'str' instead
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=algorithm,
            )
        )
    return private_key


# Génération clé publique
def generate_public_key(private_key, filename: str, config: Configuration):
    # Construction des information qui font l'objet de la certification
    subject = read_configuration(config)

    # Parce que ce certificat est auto-signé
    issuer = subject

    # Durée de validité de la clé publique (60 jours)
    valid_from = datetime.utcnow()
    valid_to = valid_from + timedelta(days=60)

    # Ajout de toutes les informations au constructeur de la clé publique, pour que l'ensemble soit signé
    builder = (
        x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(valid_from)
            .not_valid_after(valid_to)
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True, )
    )

    # Signature du certificat avec la clé privée
    public_key = builder.sign(
        private_key, hashes.SHA256(), default_backend()
    )
    # Les lignes de 75 à 78 écrivent le cerficat dans le fichier "nomdefichier"
    with open(filename, "wb") as certfile:
        certfile.write(public_key.public_bytes(serialization.Encoding.PEM))

    return public_key


# Génération du fichier de requête de certification
def generate_csr(private_key, filename: str, config: Configuration):
    # Construction des informations qui font l'objet de la certification
    subject = read_configuration(config)

    # Génération des alternatives de serveurs DNS valides pour le certificat
    alt_names = []
    for name in config.alt_names:
        alt_names.append(x509.DNSName(name))
    san = x509.SubjectAlternativeName(alt_names)

    # Génération des différents constructeurs d'objet des attributs du CSR
    builder = (
        x509.CertificateSigningRequestBuilder()
            .subject_name(subject)
            .add_extension(san, critical=False)
    )

    # Signature du CSR avec la clé privée
    csr = builder.sign(private_key, hashes.SHA256(), default_backend())

    # Écriture de la requête de signature du certificat dans le fichier PEM
    with open(filename, "wb") as csrfile:
        # FIXME Expected type 'Encoding', got 'str' instead
        csrfile.write(csr.public_bytes(serialization.Encoding.PEM))

    return csr


# Création de la clé publique signée par le ca
def sign_csr(csr, ca_public_key, ca_private_key, filename: str):
    # Definition de la validité du certificat qui sera géneré à 60 jours
    valid_from = datetime.utcnow()
    valid_until = valid_from + timedelta(days=60)

    # Attributs du certificat
    builder = (
        x509.CertificateBuilder()
            .subject_name(csr.subject)  # l'objet est bien celui du CSR
            .issuer_name(ca_public_key.subject)  # issuer est le ca
            .public_key(csr.public_key())  # obtient la clé publique du CSR.
            .serial_number(x509.random_serial_number())
            .not_valid_before(valid_from)
            .not_valid_after(valid_until)
    )

    # Ajoute les extentions existantes dans le certificat csr
    for extension in csr.extensions:
        builder = builder.add_extension(extension.value, extension.critical)

    # Signature de la clé publique avec la clé privée du ca
    public_key = builder.sign(
        private_key=ca_private_key,
        algorithm=hashes.SHA256(),
        backend=default_backend(),
    )

    # Génération du cerficat signée par le ca
    with open(filename, "wb") as keyfile:
        # FIXME Expected type 'Encoding', got 'str' instead
        keyfile.write(public_key.public_bytes(serialization.Encoding.PEM))
