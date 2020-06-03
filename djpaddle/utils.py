import base64
import collections

import phpserialize
from Crypto.PublicKey import RSA

try:
    from Crypto.Hash import SHA1
except ImportError:  # pragma: no cover
    from Crypto.Hash import SHA as SHA1

try:
    from Crypto.Signature import PKCS1_v1_5
except ImportError:  # pragma: no cover
    from Crypto.Signature import pkcs1_15 as PKCS1_v1_5


PADDLE_DATE_FORMAT = "%Y-%m-%d"
PADDLE_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def convert_pubkey_to_rsa(key):
    """
    convert key from PEM to DER - Strip the first and last lines and newlines,
    decode and return an instance of `Crypto.PublicKey.RSA`
    """
    public_key_encoded = "".join(key.split("\n")[1:-1])
    public_key_der = base64.b64decode(public_key_encoded)
    return RSA.importKey(public_key_der)


def is_valid_webhook(payload):
    data = dict(payload)
    signature = data.pop("p_signature", None)
    if signature is None:
        return False

    # Ensure all the data fields are strings
    for field in data:
        data[field] = str(data[field])

    # Sort the data and serialize it
    sorted_data = collections.OrderedDict(sorted(data.items()))
    serialized_data = phpserialize.dumps(sorted_data)

    # verify the data
    digest = SHA1.new()
    digest.update(serialized_data)
    signature = base64.b64decode(signature)

    from . import settings

    verifier = PKCS1_v1_5.new(settings.DJPADDLE_KEY)

    return verifier.verify(digest, signature)
