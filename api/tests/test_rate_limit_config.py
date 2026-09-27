from app.config import get_settings
from app.main import app

def test_completions_rate_limit_setting():
    """Verify that the completions rate limit setting defaults to 20/minute."""
    settings = get_settings()
    assert settings.completions_rate_limit == "20/minute"

def test_limiter_exists_on_app_state():
    """Verify that the slowapi limiter is correctly initialized on the app state."""
    assert hasattr(app.state, "limiter")
    assert app.state.limiter is not None
