import json
import pathlib
import platform
import sys
import sysconfig


def get_python_version() -> tuple[int, int]:
    major: int = sys.version_info.major
    minor: int = sys.version_info.minor
    return (major, minor)


def is_windows() -> bool:
    return platform.system() == "Windows"


def descent(path: pathlib.Path, depth: int) -> pathlib.Path:
    for _ in range(depth):
        path = path.parent
    return path


def get_muskox_root() -> pathlib.Path:
    script = pathlib.Path(__file__).resolve()
    return descent(script, depth=3)


def get_python_root() -> pathlib.Path:
    return pathlib.Path(sysconfig.get_path("data"))


def get_srcs() -> list[pathlib.Path]:
    major, minor = get_python_version()

    if is_windows():
        libpath = get_python_root().joinpath("libs")
        pattern: str = f"python{major}{minor}.lib"
        return list(libpath.rglob(pattern))

    else:
        libpath = pathlib.Path(sysconfig.get_config_var("LIBDIR"))
        pattern: str = f"libpython{major}{minor}.so"
        return list(libpath.rglob(pattern))


def get_hdrs() -> list[pathlib.Path]:
    include_directory = pathlib.Path(sysconfig.get_path("include"))
    return list(include_directory.rglob("*.h"))


def get_includes() -> list[pathlib.Path]:
    include_directory = pathlib.Path(sysconfig.get_path("include"))
    internal_directories = [
        path
        for path in include_directory.iterdir()
        if path.is_dir()
    ]
    return [include_directory] + internal_directories


def main():
    if pathlib.Path.cwd() != get_muskox_root():
        raise RuntimeError("The script must be run from the 'muskox' root")

    root: str = get_python_root().as_posix()

    srcs: list[str] = [
        src.relative_to(root).as_posix()
        for src in get_srcs()
    ]

    if not srcs:
        raise RuntimeError("The script did not detect any of source files")

    hdrs: list[str] = [
        hdr.relative_to(root).as_posix()
        for hdr in get_hdrs()
    ]

    if not hdrs:
        raise RuntimeError("The script did not detect any of header files")

    includes: list[str] = [
        include.relative_to(root).as_posix()
        for include in get_includes()
    ]

    root_as_text: str = f"\"{root}\""
    srcs_as_text: str = json.dumps(srcs, indent=4)
    hdrs_as_text: str = json.dumps(hdrs, indent=4)
    includes_as_text: str = json.dumps(includes, indent=4)

    text: str = "\n".join([
        "\"\"\"",
        "# This file is automatically generated by the build script.",
        "# Do not modify this file -- YOUR CHANGES WILL BE ERASED!",
        "\"\"\"\n",
        f"ROOT = {root_as_text}\n",
        f"SRCS = {srcs_as_text}\n",
        f"HDRS = {hdrs_as_text}\n",
        f"INCLUDES = {includes_as_text}\n",
    ])

    with open("bazel/env/cpython.bzl", mode="w") as file:
        file.write(text)


if __name__ == "__main__":
    main()
