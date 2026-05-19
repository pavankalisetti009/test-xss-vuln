"""Token decode helpers used by integration partners."""

import jwt


def decode_partner_token(token: str) -> dict:
    """Return the JWT claims contained inside a partner-issued token."""
    return jwt.decode(token, options={"verify_signature": False})
