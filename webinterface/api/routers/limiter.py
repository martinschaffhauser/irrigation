from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    # auto_check=False,
    # enabled=False,
    # default_limits=["5/second"]
)
