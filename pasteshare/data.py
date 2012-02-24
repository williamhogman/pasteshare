import brukva

_client = brukva.Client("localhost",6379)

_client.connect()
_client.select(4)

def get_client():
    return _client
