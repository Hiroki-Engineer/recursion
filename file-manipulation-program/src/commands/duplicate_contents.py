import logging
from pathlib import Path

import typer

from commands.utils import validate_file_exist

app = typer.Typer()

_logger = logging.getLogger()


@app.command("duplicate-contents")
def duplicate_contents(inputpath: Path, n: int) -> None:
    _logger.info(f"inputpath: {inputpath.resolve()}\nn: {n}\n")

    validate_file_exist(inputpath)

    with inputpath.open("r") as f:
        content = f.read()

    with inputpath.open("w") as f:
        for _ in range(n):
            f.write(content)
