"""
Lab 8.2: Custom Exception Hierarchy
====================================

Design and implement a custom exception system for a REST API.
Practice creating exception hierarchies, adding context, and
converting exceptions to API-friendly error responses.
"""


# ============================================================
# Part 1: Define the Exception Hierarchy
# ============================================================

class APIError(Exception):
    """
    Base exception for all API errors.

    Attributes:
    - message: human-readable error description
    - status_code: HTTP status code (default 500)
    - error_code: machine-readable error code (e.g., "INTERNAL_ERROR")
    """

    def __init__(self, message: str, status_code: int = 500, error_code: str = "INTERNAL_ERROR"):
        # TODO: Store attributes and call super().__init__(message)
        pass

    def to_dict(self) -> dict:
        """
        Convert the exception to an API response dict.

        Return: {"error": error_code, "message": message, "status": status_code}
        """
        # TODO: Implement
        pass


class NotFoundError(APIError):
    """
    Raised when a requested resource doesn't exist.
    Default status_code: 404, error_code: "NOT_FOUND"
    """
    # TODO: Implement __init__ that sets correct defaults
    pass


class ValidationError(APIError):
    """
    Raised when request data fails validation.
    Default status_code: 400, error_code: "VALIDATION_ERROR"

    Additional attribute:
    - field: the name of the invalid field (optional)
    """
    # TODO: Implement __init__ with optional 'field' parameter
    pass


class AuthenticationError(APIError):
    """
    Raised when authentication fails.
    Default status_code: 401, error_code: "AUTH_FAILED"
    """
    # TODO: Implement
    pass


class RateLimitError(APIError):
    """
    Raised when rate limit is exceeded.
    Default status_code: 429, error_code: "RATE_LIMITED"

    Additional attribute:
    - retry_after: seconds until the client can retry (int)
    """
    # TODO: Implement with retry_after attribute
    pass


# ============================================================
# Part 2: Use the Exceptions in a Mock API
# ============================================================

USERS_DB = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
}

REQUEST_COUNTS = {}
RATE_LIMIT = 5


def get_user(user_id: int, api_key: str | None = None) -> dict:
    """
    Simulate fetching a user from the API.

    Rules:
    1. If api_key is None, raise AuthenticationError
    2. Track requests per api_key; if > RATE_LIMIT, raise RateLimitError(retry_after=60)
    3. If user_id is not a positive integer, raise ValidationError for field "user_id"
    4. If user_id not in USERS_DB, raise NotFoundError
    5. Otherwise, return the user dict

    TODO: Implement all validation and error handling
    """
    # TODO: Implement
    pass


def handle_request(func, *args, **kwargs) -> dict:
    """
    Call func and return a standardized response dict.

    On success: {"status": 200, "data": <result>}
    On APIError: the error's to_dict() output
    On any other exception: {"error": "INTERNAL_ERROR", "message": str(e), "status": 500}
    """
    # TODO: Implement
    pass


# ============================================================
# Tests
# ============================================================

def test_hierarchy():
    assert issubclass(NotFoundError, APIError)
    assert issubclass(ValidationError, APIError)
    assert issubclass(AuthenticationError, APIError)
    assert issubclass(RateLimitError, APIError)
    assert issubclass(APIError, Exception)
    print("✓ Exception hierarchy is correct")


def test_to_dict():
    err = NotFoundError("User not found")
    d = err.to_dict()
    assert d["status"] == 404
    assert d["error"] == "NOT_FOUND"
    assert "User not found" in d["message"]
    print("✓ to_dict works correctly")


def test_validation_error():
    err = ValidationError("Invalid email format", field="email")
    assert err.status_code == 400
    assert err.field == "email"
    print("✓ ValidationError with field works")


def test_rate_limit():
    err = RateLimitError("Too many requests", retry_after=60)
    assert err.status_code == 429
    assert err.retry_after == 60
    print("✓ RateLimitError with retry_after works")


def test_get_user():
    # Reset state
    REQUEST_COUNTS.clear()

    # No API key
    result = handle_request(get_user, 1)
    assert result["status"] == 401

    # Valid request
    result = handle_request(get_user, 1, api_key="key123")
    assert result["status"] == 200
    assert result["data"]["name"] == "Alice"

    # Not found
    result = handle_request(get_user, 999, api_key="key123")
    assert result["status"] == 404

    # Invalid ID
    result = handle_request(get_user, -1, api_key="key123")
    assert result["status"] == 400

    print("✓ get_user error handling works")


def test_rate_limiting():
    REQUEST_COUNTS.clear()
    for i in range(RATE_LIMIT):
        result = handle_request(get_user, 1, api_key="flood_key")
        assert result["status"] == 200, f"Request {i+1} should succeed"

    result = handle_request(get_user, 1, api_key="flood_key")
    assert result["status"] == 429
    print("✓ Rate limiting works")


if __name__ == "__main__":
    test_hierarchy()
    test_to_dict()
    test_validation_error()
    test_rate_limit()
    test_get_user()
    test_rate_limiting()
    print("\nAll tests passed! ✓")
