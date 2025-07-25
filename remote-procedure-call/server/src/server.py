import asyncio
import logging
import struct
from pathlib import Path

from request_model import RequestBaseModel


class UnixSocketServer:
    def __init__(self, socket_path: Path) -> None:
        self.socket_path = socket_path
        self.server: asyncio.AbstractServer | None = None
        self.logger = logging.getLogger(__name__)

    async def start(self) -> None:
        self.socket_path.unlink(missing_ok=True)

        self.server = await asyncio.start_unix_server(self.handle_client, path=str(self.socket_path))

        self.logger.info("Starting...")
        try:
            async with self.server:
                await self.server.serve_forever()
        except asyncio.CancelledError:
            self.logger.info("Server is shutting down...")
        finally:
            self.logger.info("Stopped")
            self.socket_path.unlink(missing_ok=True)

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            # There is only one socket file, but each accepted connection gets a new file descriptor (FD).
            # This log confirms that behavior.
            sock = writer.get_extra_info("socket")
            if sock is not None:
                self.logger.info(f"Client connected with FD: {sock.fileno()}")
            else:
                self.logger.warning("Could not retrieve socket info.")

            length_bytes = await reader.readexactly(4)
            msg_length = struct.unpack("!I", length_bytes)[0]
            data = await reader.readexactly(msg_length)

            message = data.decode(encoding="utf-8")
            self.logger.info(f"Received Message: {message}")

            result = self.create_result(message)
            self.logger.info(f"Result: {result}")

            result_data = result.encode(encoding="utf-8")
            result_length = struct.pack("!I", len(result_data))

            writer.write(result_length + result_data)
            await writer.drain()

        finally:
            writer.close()
            await writer.wait_closed()

    def create_result(self, message: str) -> str:
        request_model = RequestBaseModel.model_validate_json(message)
        function_model = request_model.parse_function_model()
        result = function_model.result()
        result.id = request_model.id
        return result.model_dump_json()
