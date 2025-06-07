from pathlib import Path


class SpecifiedFileNotFoundError(FileNotFoundError):
    def __init__(self, file_path: Path) -> None:
        super().__init__(f"The specified input file does not exist: {file_path}")


def validate_file_exist(file_path: Path) -> None:
    if not file_path.is_file():
        raise SpecifiedFileNotFoundError(file_path)
