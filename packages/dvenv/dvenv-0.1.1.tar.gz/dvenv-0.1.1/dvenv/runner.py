from dvenv import log
from dvenv.decorators import with_client


@with_client
def python(client):
    client.run_python()
