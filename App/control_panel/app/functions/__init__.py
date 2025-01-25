import secrets


def generate_secret_key():
    """Generates a secure secret key for a Flask application."""
    return secrets.token_hex(32)
