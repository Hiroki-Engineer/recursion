import asyncio
from pathlib import Path

from logging_config import setup_logging
from server import UnixSocketServer

SOCKET_PATH = Path(__file__).parent.parent.parent / "unix_socket"


def main() -> None:
    server = UnixSocketServer(socket_path=SOCKET_PATH)
    asyncio.run(server.start())


if __name__ == "__main__":
    setup_logging()
    main()
