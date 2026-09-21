class AuthenticationError(Exception):
	"""Base exception for reusable authentication failures."""


class InvalidPasswordError(AuthenticationError, ValueError):
	"""The password does not satisfy the configured policy."""


class InvalidCredentialsError(AuthenticationError, ValueError):
	"""The supplied identifier or password is invalid."""
