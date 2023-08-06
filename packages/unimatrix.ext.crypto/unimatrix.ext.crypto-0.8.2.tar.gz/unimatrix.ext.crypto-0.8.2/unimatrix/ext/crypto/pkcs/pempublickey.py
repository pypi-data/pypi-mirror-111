"""Declares :class:`PEMPublicKey`."""
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers

from .pkcspublic import PKCSPublic


class PEMPublicKey(PKCSPublic):

    @property
    def bytes(self) -> bytes:
        """Return a byte sequence holding the public key."""
        return self._public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    @classmethod
    def frompem(cls, pem: bytes) -> PKCSPublic:
        if isinstance(pem, str):
            pem = str.encode(pem)
        return cls(serialization.load_pem_public_key(pem))

    def __init__(self, key):
        self._public = key


class RSAPublicKey(PEMPublicKey):

    @property
    def e(self):
        return self._numbers.e

    @property
    def n(self):
        return self._numbers.n

    @property
    def keyid(self):
        h = hashlib.md5() # nosec
        h.update(int.to_bytes(self.e, 32, 'big'))
        h.update(int.to_bytes(self.n, 512, 'big'))
        return h.hexdigest()

    @classmethod
    def fromjwk(cls, jwk):
        return cls.fromnumbers(
            int.from_bytes(jwk.e, 'big'),
            int.from_bytes(jwk.n, 'big'),
        )

    @classmethod
    def fromnumbers(cls, e, n):
        assert isinstance(e, int) # nosec
        assert isinstance(n, int) # nosec
        return cls(RSAPublicNumbers(e, n).public_key())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._numbers = self._public.public_numbers()
