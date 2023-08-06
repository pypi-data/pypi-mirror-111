import sys
from dvenv import log
from dvenv.decorators import with_client


@with_client
def python(client):
    args = sys.argv[1:]
    client.run_python(*args)
