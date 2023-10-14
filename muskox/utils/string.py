import random
import string

RANDOM_STRING_MINLEN: int = 0
RANDOM_STRING_MAXLEN: int = 512


def random_string(
    chars: str = string.ascii_letters,
    minlen: int = RANDOM_STRING_MINLEN,
    maxlen: int = RANDOM_STRING_MAXLEN,
) -> str:
    if not isinstance(chars, str):
        raise TypeError("The argument 'chars' must be 'str'")

    if not isinstance(minlen, int):
        raise TypeError("The argument 'minlen' must be 'int'")

    if not isinstance(maxlen, int):
        raise TypeError("The argument 'maxlen' must be 'int'")

    if not chars:
        raise ValueError("The argument 'chars' must be non-empty")

    if minlen < 0:
        raise ValueError("The argument 'minlen' must be positive")

    if maxlen < 0:
        raise ValueError("The argument 'maxlen' must be positive")

    return "".join([random.choice(chars) for _ in range(minlen, maxlen)])
