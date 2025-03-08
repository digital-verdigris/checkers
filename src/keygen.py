from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import Name, NameAttribute, CertificateBuilder
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import datetime
import os

class checkers_keygen:
    def __init__(self, player_name):
        self.player_name = player_name
        self.keys_directory = "keys"

    def generate_private_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        return private_key

    def generate_public_key(self, private_key):
        return private_key.public_key()

    def generate_certificate(self, private_key, public_key):
        subject = issuer = Name([
            NameAttribute(NameOID.COUNTRY_NAME, u"US"),
            NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Oregon"),
            NameAttribute(NameOID.LOCALITY_NAME, u"Eugene"),
            NameAttribute(NameOID.ORGANIZATION_NAME, u"Digital Verdigris"),
            NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        builder = CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(public_key).serial_number(1000)
        builder = builder.not_valid_before(datetime.datetime.utcnow()).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        certificate = builder.sign(private_key, hashes.SHA256())
        
        return certificate

    def save_keys(self, private_key, certificate):
        if not os.path.exists(self.keys_directory):
            os.makedirs(self.keys_directory)

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        private_key_filename = os.path.join(self.keys_directory, f"{self.player_name}_private_key.pem")
        with open(private_key_filename, "wb") as f:
            f.write(private_pem)
        print(f"Private key saved as {private_key_filename}")
        
        cert_pem = certificate.public_bytes(serialization.Encoding.PEM)
        
        cert_filename = os.path.join(self.keys_directory, f"{self.player_name}_certificate.pem")
        with open(cert_filename, "wb") as f:
            f.write(cert_pem)
        print(f"Certificate saved as {cert_filename}")
        pass

    def generate_keys_and_certificate(self):
        private_key = self.generate_private_key()
        public_key = self.generate_public_key(private_key)
        certificate = self.generate_certificate(private_key, public_key)
        self.save_keys(private_key, certificate)