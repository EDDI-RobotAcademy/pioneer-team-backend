import base64
import hashlib
import hmac
import json
import time


class GateTokenError(Exception):
    pass


class GateTokenSecretMissingError(GateTokenError):
    pass


class GateTokenInvalidError(GateTokenError):
    pass


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _sign(payload_encoded: str, secret: str) -> bytes:
    return hmac.new(
        secret.encode("utf-8"),
        payload_encoded.encode("ascii"),
        hashlib.sha256,
    ).digest()


def issue_token(
    secret: str | None,
    ttl_seconds: int,
    *,
    now: int | None = None,
) -> str:
    if not secret:
        raise GateTokenSecretMissingError(
            "토큰 시크릿이 설정되지 않았습니다."
        )
    if ttl_seconds <= 0:
        raise GateTokenError("TTL은 0보다 큰 값이어야 합니다.")

    issued_at = now if now is not None else int(time.time())
    expires_at = issued_at + ttl_seconds
    payload = json.dumps(
        {"iat": issued_at, "exp": expires_at}, separators=(",", ":")
    )
    payload_encoded = _b64url_encode(payload.encode("utf-8"))
    signature_encoded = _b64url_encode(_sign(payload_encoded, secret))
    return f"{payload_encoded}.{signature_encoded}"


def verify_token(
    token: str | None,
    secret: str | None,
    *,
    now: int | None = None,
) -> None:
    if not secret or not token:
        raise GateTokenInvalidError("invalid")

    parts = token.split(".")
    if len(parts) != 2:
        raise GateTokenInvalidError("invalid")

    payload_encoded, signature_encoded = parts
    try:
        actual_signature = _b64url_decode(signature_encoded)
    except (ValueError, TypeError) as exc:
        raise GateTokenInvalidError("invalid") from exc

    expected_signature = _sign(payload_encoded, secret)
    if not hmac.compare_digest(expected_signature, actual_signature):
        raise GateTokenInvalidError("invalid")

    try:
        payload_bytes = _b64url_decode(payload_encoded)
        payload = json.loads(payload_bytes)
        expires_at = int(payload["exp"])
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise GateTokenInvalidError("invalid") from exc

    current = now if now is not None else int(time.time())
    if current >= expires_at:
        raise GateTokenInvalidError("invalid")
