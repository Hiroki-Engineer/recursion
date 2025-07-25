import * as net from "net";
import * as path from "path";

function createRequest(id: number) {
  return {
    method: "floor",
    params: [123.6],
    param_types: ["double"],
    id: id,
  };
}

async function sendRequest(socketPath: string, messageObj: any): Promise<void> {
  return new Promise((resolve, reject) => {
    const client = net.createConnection({ path: socketPath }, () => {
      const jsonString = JSON.stringify(messageObj);
      const jsonBuffer = Buffer.from(jsonString, "utf-8");

      const lengthBuffer = Buffer.alloc(4);
      lengthBuffer.writeUInt32BE(jsonBuffer.length, 0);

      client.write(Buffer.concat([lengthBuffer, jsonBuffer]));
    });

    let responseLength = 0;
    let responseData = Buffer.alloc(0);
    let receivedHeader = false;

    client.on("data", (chunk) => {
      if (!receivedHeader) {
        if (chunk.length >= 4) {
          responseLength = chunk.readUInt32BE(0);
          responseData = chunk.slice(4);
          receivedHeader = true;
        } else {
          responseData = Buffer.concat([responseData, chunk]);
          if (responseData.length >= 4) {
            responseLength = responseData.readUInt32BE(0);
            responseData = responseData.slice(4);
            receivedHeader = true;
          }
        }
      } else {
        responseData = Buffer.concat([responseData, chunk]);
      }

      if (receivedHeader && responseData.length >= responseLength) {
        const responseString = responseData.slice(0, responseLength).toString("utf-8");
        console.log(`Response (id=${messageObj.id}):`, responseString);
        client.end();
        resolve();
      }
    });

    client.on("error", (err) => {
      reject(err);
    });
  });
}

(async () => {
  const SOCKET_PATH = path.resolve("./../unix_socket");

  const clients = [1, 2, 3, 4].map((id) => sendRequest(SOCKET_PATH, createRequest(id)));

  try {
    await Promise.all(clients);
  } catch (e) {
    console.error("Error:", e);
  }
})();
