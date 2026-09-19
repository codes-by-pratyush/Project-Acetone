import pytest
from backend.app.core.security import get_password_hash, verify_password

def test_password_hashing():
    raw = "SecurePassword123!"
    hashed = get_password_hash(raw)
    assert verify_password(raw, hashed) is True
