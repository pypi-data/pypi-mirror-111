"""Declares :class:`Verifier`."""
import abc

from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.exceptions import InvalidSignature


class Verifier(metaclass=abc.ABCMeta):
    """Declares an interface to verify signatures."""

    @abc.abstractmethod
    def verify(self, signature):
        """Return a boolean indicating if `signature` is valid."""
        raise NotImplementedError


class LocalVerifier(Verifier):
    """A :class:`Verifier` implementation that uses a local
    public key.
    """

    @abc.abstractproperty
    def key(self):
        raise NotImplementedError

    def verify(self, signature: bytes, digest: bytes,
        padding, algorithm, prehashed=True, *args, **kwargs) -> bytes:
        algorithm = utils.Prehashed(algorithm)
        try:
            self.key.verify(bytes(signature), digest, padding, algorithm)
            return True
        except InvalidSignature:
            return False

