import hmac
import hashlib

class OPRFServer:
    def __init__(self, key: bytes):
        self.key = key

    def evaluate(self, x: str) -> bytes:
        return hmac.new(self.key, x.encode(), hashlib.sha256).digest()