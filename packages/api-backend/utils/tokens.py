"""Token decode helpers used by integration partners."""

import jwt


def decode_partner_token(token: str) -> dict:
    """Return the claims embedded in a partner-issued JWT."""
    return jwt.decode(token, options={"verify_signature": False})
