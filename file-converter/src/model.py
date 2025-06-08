from pathlib import Path

from pydantic import BaseModel, field_validator

ARGS_LENGTH = 4


class ArgvLengthValueError(ValueError):
    def __init__(self, argv: list[str], length: int) -> None:
        super().__init__(f"'{argv}' must be {length} length.")


class CommandNotFoundError(ValueError):
    def __init__(self, command: str) -> None:
        super().__init__(f"'{command}' command does not exist.")


class SpecifiedFileNotFoundError(FileNotFoundError):
    def __init__(self, file_path: Path) -> None:
        super().__init__(f"The specified input file does not exist: {file_path}")


class InvalidExtentsionError(ValueError):
    def __init__(self, file_path: Path, extension: str) -> None:
        super().__init__(f"'{file_path}' must be '.{extension}' file.")


class Args(BaseModel):
    python_file: str
    command: str
    inputfile: Path
    outputfile: Path

    @classmethod
    def from_argv(cls, argv: list[str]) -> "Args":
        if len(argv) != ARGS_LENGTH:
            raise ArgvLengthValueError(argv, ARGS_LENGTH)
        return cls(
            python_file=argv[0],
            command=argv[1],
            inputfile=Path(argv[2]),
            outputfile=Path(argv[3]),
        )

    @field_validator("command", mode="before")
    @classmethod
    def validate_command(cls, value: str) -> str:
        if value != "markdown":
            raise CommandNotFoundError(value)
        return value

    @field_validator("inputfile", mode="before")
    @classmethod
    def validate_inputfile(cls, value: Path) -> Path:
        if not value.is_file():
            raise SpecifiedFileNotFoundError(value)
        if not value.suffix != "md":
            raise InvalidExtentsionError(value, value.suffix)
        return value

    @field_validator("outputfile", mode="before")
    @classmethod
    def validate_outputfile(cls, value: Path) -> Path:
        if not value.suffix != "html":
            raise InvalidExtentsionError(value, value.suffix)
        return value
