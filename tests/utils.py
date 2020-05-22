import os

from Crypto.PublicKey import RSA

DEFAULT_KEY_SIZE = 1024  # minimum = 1024


def generate_private_key(size=None):
    """
    generates a RSA public/private keypair to generate and verify webhook signatures
    """
    return RSA.generate(size or DEFAULT_KEY_SIZE, os.urandom)


def export_pubkey_as_pem(key):
    """
    exports the public key of a RSA public/private keypair in PEM format, which is
    used by paddle and intended to be set as `settings.DJPADDLE_PUBLIC_KEY`
    """
    return key.publickey().exportKey("PEM").decode("utf-8")
