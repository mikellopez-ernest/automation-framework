from __future__ import annotations

import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from automation.api.dependencies import SettingsDependency

bearer_scheme = HTTPBearer(
    auto_error=False,
)


def require_api_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    settings: SettingsDependency,
) -> None:
    """Validate the static API bearer token."""
    configured_token = settings.api_token

    if not configured_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": {
                    "code": "api_token_not_configured",
                    "message": "The API token is not configured.",
                }
            },
        )

    if (
        credentials is None
        or credentials.scheme.lower() != "bearer"
        or not secrets.compare_digest(
            credentials.credentials,
            configured_token,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "unauthorized",
                    "message": "Invalid or missing API token.",
                }
            },
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )


ApiTokenDependency = Annotated[
    None,
    Depends(require_api_token),
]
