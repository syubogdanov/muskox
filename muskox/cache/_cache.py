import datetime
import hashlib
import pathlib
import tempfile
import typing


def hexhash(key: str) -> str:
    return hashlib.md5(key.encode()).hexdigest()


def get_cache_dir() -> pathlib.Path:
    dir = pathlib.Path(tempfile.gettempdir()) / "muskox"
    dir.mkdir(parents=True, exist_ok=True)
    return dir


def upload(key: str, path: pathlib.Path):
    if not isinstance(key, str):
        raise TypeError("The argument 'key' must be 'str'")

    if not isinstance(path, pathlib.Path):
        raise TypeError("The argument 'path' must be 'pathlib.Path'")

    symlink: pathlib.Path = get_cache_dir() / hexhash(key)
    symlink.unlink(missing_ok=True)

    try:
        assert path.exists(), "The cached path does not exist"
        symlink.symlink_to(path.resolve(), path.is_dir())

    except OSError:
        pass

    except Exception as exception:
        raise exception


def load(key: str) -> typing.Optional[pathlib.Path]:
    if not isinstance(key, str):
        raise TypeError("The argument 'key' must be 'str'")

    symlink: pathlib.Path = get_cache_dir() / hexhash(key)

    if not symlink.exists(follow_symlinks=False):
        return None

    if not symlink.exists(follow_symlinks=True):
        return None

    assert symlink.is_symlink()
    return symlink.resolve()


def clean(timeout: float = 3.0):
    for symlimk in get_cache_dir().glob("*"):
        mtime: float = symlimk.stat(follow_symlinks=False).st_mtime

        lhs: datetime.datetime = datetime.datetime.fromtimestamp(mtime)
        rhs: datetime.datetime = datetime.datetime.now()

        seconds: int = (rhs - lhs).seconds
        hours: float = seconds / (60 * 60)

        if symlimk.is_symlink() and hours > timeout:
            symlimk.unlink()


def clear():
    for symlimk in get_cache_dir().glob("*"):
        if symlimk.is_symlink():
            symlimk.unlink()
