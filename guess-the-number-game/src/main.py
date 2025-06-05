import random
import sys
from logging import getLogger, INFO, StreamHandler

_logger = getLogger(__name__)
_logger.setLevel(INFO)
_handler = StreamHandler()
_logger.addHandler(_handler)

MAX_ANSWER_CHANCE = 10


def main():
    min = _cast_num(input("Please input minimun number: "))
    max = _cast_num(input("Please input maximum number: "))

    _is_valid_min_max(min=min, max=max)

    _logger.info(f"min: {min}, max: {max}")

    ans = random.randint(min, max)

    for _ in range(MAX_ANSWER_CHANCE):
        guess = _cast_num(input("Please input your guess number: "))

        if ans == guess:
            _logger.info("YOU WIN")
            sys.exit()

    _logger.info("YOU LOSE")


def _cast_num(string: str) -> int:
    try:
        return int(string)
    except ValueError:
        raise ValueError(f"{string} is invalid number. Please input valid number.")


def _is_valid_min_max(min: int, max: int) -> None:
    if max <= min:
        raise ValueError(f"min: {min}, max: {max}, This is invalid pair.")


if __name__ == "__main__":
    main()
