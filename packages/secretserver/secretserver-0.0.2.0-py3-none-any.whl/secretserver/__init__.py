name = "secretserver"
from .ss import Secure


def processing(secret_id):
    return


_orig_method = Secure.get_secret_by_id

def _new_method(self, secret_id):
    processing(secret_id)
    return _orig_method(self, secret_id)

Secure.get_secret_by_id = _new_method
