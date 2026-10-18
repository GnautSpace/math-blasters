import pytest
from pydantic import ValidationError

from app.config import Settings
from app.main import app


def test_completions_rate_limit_setting(monkeypatch):
    """Verify that the completions rate limit setting defaults to 20/minute."""
    monkeypatch.delenv("COMPLETIONS_RATE_LIMIT", raising=False)
    settings = Settings(_env_file=None)
    assert settings.completions_rate_limit == "20/minute"


def test_limiter_exists_on_app_state():
    """Verify that the slowapi limiter is correctly initialized on the app state."""
    assert hasattr(app.state, "limiter")
    assert app.state.limiter is not None


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ("abc", "Invalid rate limit format"),
        ("", "Invalid rate limit format"),
        ("0/minute", "Rate limit amount must be at least 1"),
    ],
)
def test_bad_completions_rate_limit_is_rejected(value, message):
    with pytest.raises(ValidationError, match=message):
        Settings(_env_file=None, completions_rate_limit=value)


def test_multiple_completions_rate_limits_are_accepted():
    settings = Settings(_env_file=None, completions_rate_limit="20/minute;100/hour")
    assert settings.completions_rate_limit == "20/minute;100/hour"
