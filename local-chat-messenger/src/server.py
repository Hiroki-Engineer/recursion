import logging
import sys
from pathlib import Path
from socket import AF_UNIX, SOCK_STREAM, socket

from const import ENCOSING_CODE, EXIT_MESSAGE

_logger = logging.getLogger()


def start_server(server_address: Path) -> None:
    _logger.info("Starting Server...")
    with socket(family=AF_UNIX, type=SOCK_STREAM) as sock:
        sock.bind(str(server_address))
        sock.listen(1)

        while True:
            conn, client_address = sock.accept()
            _logger.info("Server accepting now...")

            while True:
                data = conn.recv(32)

                if data:
                    data_str = data.decode(ENCOSING_CODE)

                    response = f"Processing {data_str}" if data_str != EXIT_MESSAGE else EXIT_MESSAGE
                    _logger.info(response)
                    conn.sendall(response.encode(ENCOSING_CODE))

                    if data_str == EXIT_MESSAGE:
                        _logger.info("Ending Server...")
                        sys.exit(0)
                else:
                    _logger.info(f"No data from {client_address}")
