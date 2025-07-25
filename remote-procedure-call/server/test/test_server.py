import asyncio
import contextlib
import json
import logging
import struct
from pathlib import Path

import pytest
from _pytest.logging import LogCaptureFixture

from server import UnixSocketServer


@pytest.mark.asyncio
async def test_unix_socket_server_communication(tmp_path: Path, caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    socket_path = tmp_path / "test_socket"

    server = UnixSocketServer(socket_path)

    server_task = asyncio.create_task(server.start())

    # Wait briefly to ensure the server has started and is ready to accept connections
    await asyncio.sleep(0.1)

    reader, writer = await asyncio.open_unix_connection(str(socket_path))

    try:
        test_value = {"method": "floor", "params": [123.6], "param_types": ["double"], "id": 3}
        test_message = json.dumps(test_value)
        msg_bytes = test_message.encode("utf-8")
        length_prefix = struct.pack("!I", len(msg_bytes))

        writer.write(length_prefix + msg_bytes)
        await writer.drain()

        response = await reader.readexactly(4)
        response_length = struct.unpack("!I", response)[0]
        data = await reader.readexactly(response_length)

        assert json.loads(data.decode("utf-8")) == {"results": "123", "result_type": "int", "id": test_value["id"]}

    finally:
        writer.close()
        await writer.wait_closed()

    server_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await server_task

    assert any(f"Received Message: {test_message}" in r.message for r in caplog.records)
