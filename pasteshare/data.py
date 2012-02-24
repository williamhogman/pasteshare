import brukva

_client = brukva.Client("localhost",6379)

def get_client():
    return _client
