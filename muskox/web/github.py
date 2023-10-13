import os
import pathlib
import tempfile
import zipfile

from urllib.parse import urljoin
from urllib.request import urlopen
from urllib.request import urlretrieve

from typing import Optional
from typing import overload

from muskox.web.typing import URL


@overload
def urlget(user: str, repo: str) -> URL:
    ...


@overload
def urlget(user: str, repo: str, branch: str) -> URL:
    ...


def urlget(user: str, repo: str, branch: Optional[str] = None) -> URL:
    if not isinstance(user, str):
        raise TypeError("'user' must be 'str'")

    if not isinstance(repo, str):
        raise TypeError("'repo' must be 'str'")

    if not isinstance(branch, str) and branch is not None:
        raise TypeError("'branch' must be 'str' or 'None'")

    if not user:
        raise ValueError("'user' must be non-empty")

    if not repo:
        raise ValueError("'repo' must be non-empty")

    if branch is None:
        return URL(f"https://github.com/{user}/{repo}")

    if not branch:
        raise ValueError("'branch' must be non-empty")

    return URL(f"https://github.com/{user}/{repo}/tree/{branch}")


@overload
def access(user: str, repo: str) -> bool:
    ...


@overload
def access(user: str, repo: str, branch: str) -> bool:
    ...


def access(user: str, repo: str, branch: Optional[str] = None) -> bool:
    if not isinstance(user, str):
        raise TypeError("'user' must be 'str'")

    if not isinstance(repo, str):
        raise TypeError("'repo' must be 'str'")

    if not isinstance(branch, str) and branch is not None:
        raise TypeError("'branch' must be 'str' or 'None'")

    if not user:
        raise ValueError("'user' must be non-empty")

    if not repo:
        raise ValueError("'repo' must be non-empty")

    if not branch and isinstance(branch, str):
        raise ValueError("'branch' must be non-empty")

    try:
        with urlopen(urlget(user, repo, branch)):
            return True

    except Exception:
        return False


def download(user: str, repo: str, branch: str) -> pathlib.Path:
    if not isinstance(user, str):
        raise TypeError("The argument 'user' must be 'str'")

    if not isinstance(repo, str):
        raise TypeError("The argument 'repo' must be 'str'")

    if not isinstance(branch, str):
        raise TypeError("The argument 'branch' must be 'str'")

    if not user:
        raise ValueError("The argument 'user' must be non-empty")

    if not repo:
        raise ValueError("The argument 'repo' must be non-empty")

    if not branch:
        raise ValueError("The argument 'branch' must be non-empty")

    if not access(user, repo):
        raise RuntimeError(f"The repository '@{user}/{repo}' is unavailable")

    if not access(user, repo, branch):
        raise RuntimeError(f"The branch '{branch}' is unavailable")

    base = urlget(user, repo).rstrip("/") + "/"
    tail = URL(f"archive/refs/heads/{branch}.zip")

    url = urljoin(base, tail)
    assert url.startswith(base)

    archive_path, _ = urlretrieve(url)
    extract_path = tempfile.mkdtemp()

    with zipfile.ZipFile(archive_path) as archive:
        archive.extractall(extract_path)

    os.remove(archive_path)
    return pathlib.Path(extract_path)
