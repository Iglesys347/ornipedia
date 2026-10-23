"""Authentication of the administration: a single password, sent as a bearer token."""

import hmac
import time

from fastapi import Header, HTTPException, status

from src import settings

# delay added to each failed attempt, to slow down password guessing
FAILED_LOGIN_DELAY = 1


def require_admin(authorization: str | None = Header(default=None)):
    if not settings.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The administration is disabled (no password configured)",
        )
    scheme, _, password = (authorization or "").partition(" ")
    # constant time comparison
    if scheme.lower() != "bearer" or not hmac.compare_digest(
        password.encode(), settings.ADMIN_PASSWORD.encode()
    ):
        time.sleep(FAILED_LOGIN_DELAY)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
            headers={"WWW-Authenticate": "Bearer"},
        )
