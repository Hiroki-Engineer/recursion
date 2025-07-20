import logging
import sys
import time
from pathlib import Path
from socket import AF_UNIX, SOCK_STREAM, socket

from const import ENCOSING_CODE, EXIT_MESSAGE

TIMEOUT_SEONCD = 2

_logger = logging.getLogger()


def start_client(server_address: Path) -> None:
    _logger.info("Starting Client...")
    with socket(family=AF_UNIX, type=SOCK_STREAM) as sock:
        connect_server(sock=sock, server_address=server_address)
        communicate_with_server(sock=sock)


def connect_server(sock: socket, server_address: Path) -> None:
    start = time.time()
    while True:
        try:
            sock.connect(str(server_address))
            _logger.info("Client Connecting now...")
            break
        except (FileNotFoundError, ConnectionRefusedError):
            if time.time() - start > TIMEOUT_SEONCD:
                _logger.exception("Please confirm that the server is starting")
                raise


def communicate_with_server(sock: socket) -> None:
    while True:
        input_str = input()

        message = input_str.encode(ENCOSING_CODE)

        sock.sendall(message)

        sock.settimeout(TIMEOUT_SEONCD)

        while True:
            try:
                data = sock.recv(32).decode(ENCOSING_CODE)
            except TimeoutError:
                break

            if data:
                _logger.info(f"Server response: {data}")
                if data == EXIT_MESSAGE:
                    _logger.info("Ending Client...")
                    sys.exit(0)
