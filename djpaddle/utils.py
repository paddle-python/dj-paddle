import base64
import hashlib
import collections
import phpserialize

from Crypto.PublicKey import RSA

try:
    from Crypto.Hash import SHA1
except ImportError:
    from Crypto.Hash import SHA as SHA1

try:
    from Crypto.Signature import PKCS1_v1_5
except ImportError:
    from Crypto.Signature import pkcs1_15 as PKCS1_v1_5

from . import settings

# Convert key from PEM to DER - Strip the first and last lines and newlines, and decode
public_key_encoded = settings.DJPADDLE_PUBLIC_KEY[26:-25].replace("\n", "")
public_key_der = base64.b64decode(public_key_encoded)
key = RSA.importKey(public_key_der)
verifier = PKCS1_v1_5.new(key)


def is_valid_webhook(payload):
    data = dict(payload)
    signature = data.pop("p_signature")

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

    return verifier.verify(digest, signature)
