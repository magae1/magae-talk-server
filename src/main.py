import logging
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from managers.connection_manager import ConnectionManager
from clients.ice_servers_client import IceServersClient
from managers.exceptions import ConnIdAlreadyExists
from settings.config import get_settings

log = logging.getLogger(__name__)


origins = (
    ["https://magae1.github.io"]
    if get_settings().env == "production"
    else ["http://localhost:5173", "http://localhost:8000"]
)

middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
]
app = FastAPI(middleware=middlewares)


manager = ConnectionManager()
ice_client = IceServersClient()


@app.get("/healthz")
async def health_check() -> None:
    return


@app.get("/ice-servers")
async def get_ice_servers():
    return ice_client.get_ice_servers()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    conn_id = manager.generate_next_id()
    try:
        await manager.connect(conn_id, websocket)
    except ConnIdAlreadyExists as e:
        log.exception(e)
        return

    log.info(f"Start connecting...{conn_id}")
    retry_count = 0
    while True:
        if retry_count >= 5:
            log.error(f"Connection {conn_id} Failed!")
            await websocket.close()
            manager.disconnect(conn_id)
            return
        try:
            conn_ids = manager.get_conn_ids()
            conn_ids.remove(conn_id)
            await manager.send_personal_data(
                {"type": "init", "id": conn_id, "body": {"other_ids": conn_ids}},
                conn_id,
            )
            await asyncio.wait_for(websocket.receive_json(), timeout=1)
            break
        except WebSocketDisconnect:
            manager.disconnect(conn_id)
            return
        except asyncio.TimeoutError:
            retry_count += 1
            log.debug(f"retrying...{retry_count}")

    log.info(f"Connection {conn_id} established!")
    await manager.broadcast(
        {
            "type": "enter",
            "id": conn_id,
            "body": {
                "msg": f"{conn_id}님이 들어왔습니다.",
            },
        }
    )

    try:
        while True:
            data: dict = await websocket.receive_json()
            await manager.send_personal_data(data, data["id"])
    except WebSocketDisconnect:
        log.info(f"Connection ${conn_id} close")
    except RuntimeError:
        log.warning("Unexpected error occurs")
    finally:
        manager.disconnect(conn_id)
        await manager.broadcast(
            {
                "type": "leave",
                "id": conn_id,
                "body": {
                    "msg": f"{conn_id}님이 나갔습니다.",
                },
            }
        )
