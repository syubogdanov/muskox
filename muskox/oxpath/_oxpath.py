import os.path
import pathlib
import typing
import urllib.error

from gitload import bitbucket
from gitload import github

from muskox.oxpath._exceptions import EmptyPath
from muskox.oxpath._exceptions import EmptyRepository
from muskox.oxpath._exceptions import EmptyService
from muskox.oxpath._exceptions import EmptyUsername
from muskox.oxpath._exceptions import OxpathNotFound
from muskox.oxpath._exceptions import SpecificationMismatch
from muskox.oxpath._exceptions import UnsupportedService


Downloader = typing.Callable[[str, str], pathlib.Path]


SERVICE_SEP: str = "@"


def is_supported_service(service: str) -> bool:
    return service in {
        "bitbucket",
        "github",
        "host",
    }


def get_downloader(service: str) -> Downloader:
    match service:
        case "bitbucket":
            return bitbucket.download

        case "github":
            return github.download

        case _:
            raise RuntimeError("The code is unreachable")


def fetch(oxpath: str) -> pathlib.Path:
    if not isinstance(oxpath, str):
        raise TypeError("The argument 'oxpath' must be 'str'")

    if len(items := oxpath.split(SERVICE_SEP)) < 2:
        message: str = f"The oxpath does not match the specification: {oxpath}"
        raise SpecificationMismatch(message)

    if not (service := items[0]):
        raise EmptyService(f"The oxpath has an empty service: {oxpath}")

    if not is_supported_service(service):
        message: str = f"The oxpath has an unsupported service: {oxpath}"
        raise UnsupportedService(message)

    if not (service_path := SERVICE_SEP.join(items[1:])):
        raise EmptyPath(f"The oxpath has an empty service path: {oxpath}")

    if service == "host":
        if not os.path.exists(service_path):
            raise OxpathNotFound(f"The oxpath not found: {oxpath}")
        return pathlib.Path(service_path)

    items: list[str] = service_path.split("/")

    if len(items) < 1:
        raise EmptyUsername(f"The oxpath has an empty username: {oxpath}")

    if len(items) < 2:
        raise EmptyRepository(f"The oxpath has an empty repository: {oxpath}")

    if len(items) > 2:
        message: str = f"The oxpath has an ambigious service path: {oxpath}"
        raise SpecificationMismatch(message)

    username: str = items[0]
    repository: str = items[1]

    try:
        download: Downloader = get_downloader(service)
        installation: pathlib.Path = download(username, repository)
        return next(installation.iterdir())

    except urllib.error.HTTPError:
        raise OxpathNotFound(f"Could not fetch the oxpath: {oxpath}")

    except Exception as exception:
        raise exception
