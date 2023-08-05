import base64
import datetime
import enum
import secrets
import time
from typing import List, Tuple, Union, Dict, Optional

from paramiko.ecdsakey import ECDSAKey
from paramiko.ed25519key import Ed25519Key
from paramiko.message import Message
from paramiko.pkey import PKey, PublicBlob
from paramiko.rsakey import RSAKey


class CertificateBlob(PublicBlob):
    """
    A signed SSH certificate
    """

    def cert_string(self, comment: str = None) -> str:
        """
        Render a string suitable for OpenSSH authorized_keys files

        Args:
            comment: an optional comment, defaulting to the current date and time in ISO format

        Returns:
            The public key string
        """

        return "{key_type} {key_string} {comment}".format(
            key_type=self.key_type,
            key_string=base64.standard_b64encode(self.key_blob).decode(),
            comment=comment or datetime.datetime.now().isoformat()
        )


class CertificateType(enum.Enum):
    """
    The type of certificate to issue
    """

    # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L73
    USER = 1

    # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L74
    HOST = 2


class CertificateCriticalOptions(enum.Enum):
    """
    `Certificate critical options`_

    .. _Certificate critical options:
       https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L221
    """

    # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L248
    FORCE_COMMAND = "force-command"

    # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L253
    SOURCE_ADDRESS = "source-address"


class CertificateExtensions(enum.Enum):
    """
    `Certificate extensions`_

    .. _Certificate extensions:
       https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L270
    """

    # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L290
    NO_TOUCH_REQUIRED = "no-touch-required"

    # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L297
    PERMIT_X11_FORWARDING = "permit-X11-forwarding"

    # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L301
    PERMIT_AGENT_FORWARDING = "permit-agent-forwarding"

    # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L306
    PERMIT_PORT_FORWARDING = "permit-port-forwarding"

    # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L311
    PERMIT_PTY = "permit-pty"

    # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L316
    PERMIT_USER_RC = "permit-user-rc"

    @classmethod
    def permit_all(cls) -> Dict["CertificateExtensions", str]:
        """
        Convenience method to return a dict enabling all extensions

        Returns:
            All available extensions
        """
        return {
            cls.NO_TOUCH_REQUIRED: "",
            cls.PERMIT_X11_FORWARDING: "",
            cls.PERMIT_AGENT_FORWARDING: "",
            cls.PERMIT_PORT_FORWARDING: "",
            cls.PERMIT_PTY: "",
            cls.PERMIT_USER_RC: "",
        }


class CertificateParameters:
    """
    All certificate parameters needed for signing

    Args:
        valid_for: duration of certificate validity, overridden by `valid_before`

    Keyword Args:
        type (CertificateType): `type of certificate`_ to issue
        key_id (str): `key identifier`_
        serial (int): certificate `serial number`_
        principals (List[str]): list of `valid principals`_
        valid_after (int): `time after which the certificate is valid`_ (unix epoch, defaults to now)
        valid_before (int): `time before which the certificate is valid`_ (unix epoch)
        critical_opts (Dict[CertificateCriticalOptions, str]): dict of certificate `critical options`_
        extensions (Dict[CertificateExtensions, str]): dict of certificate `extensions`_

    .. _type of certificate:
       https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L169
    .. _key identifier:
       https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L172
    .. _serial number:
       https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L164
    .. _valid principals:
       https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L176
    .. _time after which the certificate is valid:
       https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L183
    .. _time before which the certificate is valid:
       https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L183
    .. _critical options:
       https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L221
    .. _extensions:
       https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L270
    """

    def __init__(self, valid_for: Optional[datetime.timedelta] = datetime.timedelta(hours=1), **kwargs):

        now = int(time.time())

        # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L83
        self.cert_type: CertificateType = kwargs.get("type", CertificateType.USER)

        # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L84
        self.key_id: str = kwargs.get("key_id", "")

        # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L82
        self.serial: int = kwargs.get("serial", 0)

        # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L85
        self.principals: List[str] = kwargs.get("principals", [])

        # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L86
        self.valid_after: int = kwargs.get("valid_after", now)

        # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L87
        self.valid_before: int = kwargs.get("valid_before", self.valid_after + valid_for.seconds)

        # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L88
        self.critical_opts: List[Tuple[CertificateCriticalOptions, str]] = sorted(
            kwargs.get("critical_options", {}).items(), key=lambda _opt: _opt[0].value
        )

        # https://github.com/openssh/openssh-portable/blob/2b71010d9b43d7b8c9ec1bf010beb00d98fa765a/PROTOCOL.certkeys#L89
        self.extensions: List[Tuple[CertificateExtensions, str]] = sorted(
            kwargs.get("extensions", {}).items(),
            key=lambda _ext: _ext[0].value,
        )


class CertificateSigningRequest:
    """
    Combines the key to be signed and the certificate parameters

    Args:
        public_key: key to sign
        cert_params: certificate parameters
    """

    _CERT_SUFFIX = "-cert-v01@openssh.com"

    def __init__(self, public_key: PKey, cert_params: CertificateParameters):
        self.cert_params = cert_params
        self.public_key = public_key

    def _get_public_parts(self) -> Message:
        """
        Get the public parts from the public key to be signed

        Returns:
            The public parts of the key to be signed
        """

        public_parts = Message()
        if isinstance(self.public_key, RSAKey):
            public_parts.add_mpint(self.public_key.public_numbers.e)
            public_parts.add_mpint(self.public_key.public_numbers.n)
        elif isinstance(self.public_key, Ed25519Key):
            pkey_msg = Message(self.public_key.asbytes())
            pkey_msg.get_string()
            public_parts.add_string(pkey_msg.get_string())
        elif isinstance(self.public_key, ECDSAKey):
            public_parts = Message()
            pkey_msg = Message(self.public_key.asbytes())
            pkey_msg.get_string()
            public_parts.add_string(pkey_msg.get_string())
            public_parts.add_string(pkey_msg.get_string())
        else:
            raise NotImplementedError(
                "Can't sign certificate of type {cert_type}.".format(cert_type=self.public_key.get_name())
            )
        return public_parts

    @staticmethod
    def _encode_options(opts: List[Tuple[Union[CertificateCriticalOptions, CertificateExtensions], str]]) -> Message:
        """
        Encodes the certificate options and extensions into the required format

        Args:
            opts: list of options / extensions to encode

        Returns:
            The encoded set of options / extensions
        """
        m = Message()
        for k, v in opts:
            m.add_string(k.value)
            if len(v) == 0:
                m.add_string("")
            else:
                opt_value = Message()
                for _v in v:
                    opt_value.add_string(_v)
                m.add_string(opt_value.asbytes())
        return m

    def sign(self, signing_key: PKey) -> CertificateBlob:
        """
        Signs the public key using the signing key

        Args:
            signing_key: CA key used for signing

        Returns:
            The signed certificate
        """
        assert signing_key.can_sign(), "Key not capable of signing."

        public_parts = self._get_public_parts()

        cert = Message()
        cert.add_string(self.public_key.get_name() + self._CERT_SUFFIX)
        cert.add_string(secrets.token_bytes(32))
        cert.add_bytes(public_parts.asbytes())
        cert.add_int64(self.cert_params.serial)
        cert.add_int(self.cert_params.cert_type.value)
        cert.add_string(self.cert_params.key_id)

        if len(self.cert_params.principals) == 0:
            cert.add_string("")
        else:
            m = Message()
            for p in self.cert_params.principals:
                m.add_string(p)
            cert.add_string(m.asbytes())

        cert.add_int64(self.cert_params.valid_after)
        cert.add_int64(self.cert_params.valid_before)

        for opts in [self.cert_params.critical_opts, self.cert_params.extensions]:
            if len(opts) == 0:
                cert.add_string("")
            else:
                cert.add_string(self._encode_options(opts).asbytes())

        cert.add_string("")
        cert.add_string(signing_key.asbytes())
        cert.add_string(signing_key.sign_ssh_data(cert.asbytes()))
        cert.rewind()

        return CertificateBlob.from_message(cert)

class CertificateSigningKeyMixin(PKey):
    """
    Mixin that allows a key to act as a certificate authority
    """

    def sign_certificate(self, pub_key: PKey, principals: List[str],
                         extensions: Dict[CertificateExtensions, str] = None, **kwargs) -> CertificateBlob:
        """
        Signs a public key to produce a certificate

        Args:
            pub_key: the SSH public key
            principals: a list of principals to encode into the certificate
            extensions: a dictionary of certificate extensions, see :py:mod:`paramiko_cloud.pki.CertificateExtensions`
            **kwargs: additional certificate configuration parameters passed to the constructor of :py:mod:`paramiko_cloud.pki.CertificateParameters`

        Returns:
            A PublicBlob object containing the signed certificate
        """
        return CertificateSigningRequest(pub_key, CertificateParameters(
            principals=principals,
            extensions=extensions or CertificateExtensions.permit_all(),
            **kwargs
        )).sign(self)