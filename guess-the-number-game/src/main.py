import random
import sys
from logging import getLogger, INFO, StreamHandler

_logger = getLogger(__name__)
_logger.setLevel(INFO)
_handler = StreamHandler()
_logger.addHandler(_handler)

MAX_ANSWER_CHANCE = 10


def main():
    min, max = _input_valid_min_max()

    _logger.info(f"min: {min}, max: {max}")

    ans = random.randint(min, max)

    counter = 0

    while counter < MAX_ANSWER_CHANCE:
        try:
            guess = _input_valid_number(
                f"Please input your guess number ({MAX_ANSWER_CHANCE - counter} chances left to answer)",
                is_raise_exc=True,
            )

        except ValueError as e:
            _logger.error(e)

        else:
            if ans == guess:
                _logger.info("YOU WIN")
                sys.exit()

        counter += 1

    _logger.info("YOU LOSE")


def _input_valid_min_max() -> tuple[int, int]:
    while True:
        min = _input_valid_number("Please input minimun number")
        max = _input_valid_number("Please input maximum number")

        if min < max:
            return min, max

        _logger.error(f"min: {min}, max: {max}, This is invalid pair.")


def _input_valid_number(message: str, is_raise_exc: bool = False) -> int:
    while True:
        string = input(message + " (or 'exit' to quit): ")

        if string == "exit":
            _logger.info("'exit' entered. Stop this game.")
            sys.exit()

        try:
            return int(string)

        except ValueError:
            err_message = f"'{string}' is invalid number. Please input valid number."

            if is_raise_exc:
                raise ValueError(err_message)

            _logger.error(err_message)


if __name__ == "__main__":
    main()
