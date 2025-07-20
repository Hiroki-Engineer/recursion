from multiprocessing import Process

from client import start_client
from const import SERVER_ADDRESS
from server import start_server
from setup_logging import setup_logging


def main() -> None:
    try:
        # Start server in background process
        server_proc = Process(target=start_server, args=(SERVER_ADDRESS,))
        server_proc.start()

        # Start client in main process
        start_client(SERVER_ADDRESS)
    finally:
        SERVER_ADDRESS.unlink(missing_ok=True)


if __name__ == "__main__":
    setup_logging()
    main()
