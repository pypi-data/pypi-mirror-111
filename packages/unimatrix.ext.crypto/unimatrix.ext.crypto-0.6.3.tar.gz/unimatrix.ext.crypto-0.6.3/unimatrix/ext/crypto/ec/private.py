"""Declares :class:`EllipticCurvePrivateKey`."""
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import utils

from .. import oid
from ..private import PrivateKey
from .public import EllipticCurvePublicKey


class EllipticCurvePrivateKey(PrivateKey):
    __algorithm_mapping = {
        'P-256K'    : oid.SECP256K1,
        'SECP256K1' : oid.SECP256K1,
    }
    capabilities = list(__algorithm_mapping.values())

    def setup(self, opts):
        """Configures the :class:`EllipticCurvePublicKey` using the given
        options `opts`. This method is called in the constructor and should not
        be called more than once.
        """
        self.__curve = ec.SECP256K1()
        self.__key = ec.derive_private_key(opts.secret, self.__curve)
        self.__public = self.__key.public_key()

    async def get_public_key(self) -> EllipticCurvePublicKey:
        return EllipticCurvePublicKey(self.__public)

    def has_public_key(self) -> bool:
        """Return a boolean indicating if the private key is able to
        extract and provide its public key.
        """
        return True

    async def sign(self,
        blob: bytes,
        hasher,
        algorithm,
        curve: ec.EllipticCurve,
        *args, **kwargs
    ) -> bytes:
        """Returns the signature of byte-sequence `blob`, DER-encoded."""
        hasher.update(blob)
        digest = hasher.finalize()
        key = self._get_key(curve)
        return key.sign(digest, ec.ECDSA(utils.Prehashed(algorithm)))

    async def verify(self,
        signature: bytes,
        blob: bytes,
        hasher,
        algorithm,
        curve,
    ) -> bytes:
        hasher.update(blob)
        digest = hasher.finalize()
        try:
            self.__public.verify(
                bytes(signature), digest,
                ec.ECDSA(utils.Prehashed(algorithm))
            )
            return True
        except InvalidSignature:
            return False

    def _get_key(self, curve):
        return self.__key
