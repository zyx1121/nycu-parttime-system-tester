import base64
import hashlib
import hmac
import time
from urllib.parse import urlparse, parse_qs


def totp(uri: str) -> str:
    """
    Input:  otpauth://totp/XXX?secret=BASE32SECRET
    Output: 6-digit TOTP (default: SHA1, 30s, 6 digits)
    """

    u = urlparse(uri.strip())
    if u.scheme != "otpauth" or u.netloc.lower() != "totp":
        raise ValueError("uri must be otpauth://totp/...")

    qs = parse_qs(u.query)
    secret = (qs.get("secret") or [None])[0]
    if not secret:
        raise ValueError("uri must have secret=...")

    # Base32 decode (allow missing '=', allow lowercase/spaces)
    s = secret.strip().replace(" ", "").upper()
    s += "=" * ((-len(s)) % 8)
    key = base64.b32decode(s, casefold=True)

    # TOTP: counter = floor(time / 30)
    counter = int(time.time()) // 30
    msg = counter.to_bytes(8, "big")

    # HOTP (RFC 4226) + dynamic truncation
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    dbc = (
        ((h[offset] & 0x7F) << 24)
        | (h[offset + 1] << 16)
        | (h[offset + 2] << 8)
        | (h[offset + 3])
    )

    code = dbc % 1_000_000
    return f"{code:06d}"
