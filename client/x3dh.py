from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

def derive_x3dh_shared_secret(dh_outputs: bytes):
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"x3dh-key-agreement",
    ).derive(dh_outputs)