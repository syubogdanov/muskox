import pathlib


def main():
    cwd: pathlib.Path = pathlib.Path.cwd()

    for file in cwd.rglob("*.py[cod]"):
        file.unlink()

    for directory in cwd.rglob("__pycache__"):
        directory.rmdir()


if __name__ == "__main__":
    main()
