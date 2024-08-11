from rest_framework.exceptions import Throttled
from rest_framework.throttling import SimpleRateThrottle


class OTPRateThrottle(SimpleRateThrottle):
    """
    Throttle class to limit OTP requests.
    """

    scope = "otp"

    def get_cache_key(self, request, view):
        phone = request.data.get("phone")
        if not phone:
            return None
        return phone


class CustomThrottle(SimpleRateThrottle):
    """
    Throttle class to limit register requests.
    """

    def __init__(self, scope=None):
        self.scope = scope or "default"
        super().__init__()

    def get_cache_key(self, request, view):
        """
        Generates and returns the cache key based on the user's IP address.
        """
        ident = self.get_ident(request)
        self.key = f"{self.scope}_{ident}"
        return self.key

    def get_history(self, cache_key):
        """
        Retrieves the request history from the cache.
        Ensures that the returned value is always a list.
        """
        history = self.cache.get(cache_key, [])
        if not isinstance(history, list):
            history = []
        return history

    def allow_request(self, request, view):
        """
        Determines whether the request should be allowed based on the throttle history.
        """
        cache_key = self.get_cache_key(request, view)
        self.history = self.get_history(cache_key)

        self.now = self.timer()
        self.history = [timestamp for timestamp in self.history if timestamp > self.now - self.duration]

        if len(self.history) >= 3:
            return self.throttle_failure()

        self.history.append(self.now)
        self.cache.set(cache_key, self.history, self.duration)

        return True

    def throttle_success(self):
        """
        Resets the throttle history on successful request.
        """
        cache_key = self.key
        if cache_key:
            self.cache.set(cache_key, [], self.duration)

    def throttle_failure(self):
        """
        Updates the throttle history on failed request.
        """
        cache_key = self.key
        self.history = self.get_history(cache_key)
        self.history.append(self.now)
        self.cache.set(cache_key, self.history, self.duration)

        return False


class RegisterThrottle(CustomThrottle):
    def __init__(self):
        super().__init__(scope="register")


class LoginThrottle(CustomThrottle):
    def __init__(self):
        super().__init__(scope="login")
