# Copyright 2021 Softwerks LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import aioredis
import asyncio
import enum
import json
import logging
from typing import Dict

from . import redis

logger: logging.Logger = logging.getLogger(__name__)


@enum.unique
class Opcode(enum.Enum):
    ADD: str = "add"
    REM: str = "rem"


async def run() -> None:
    try:
        conn: aioredis.Redis = await redis.get_connection()
        channel: aioredis.Channel = (await conn.subscribe("tournament:queue"))[0]
        async for message in channel.iter(encoding="utf-8"):
            await _handle_message(json.loads(message))
    except asyncio.CancelledError:
        conn = await redis.get_connection()
        await conn.unsubscribe(channel)


async def _handle_message(message: Dict[str, str]) -> None:
    conn: aioredis.Redis = await redis.get_connection()

    opcode: Opcode = Opcode(message["opcode"])
    user: str = message["user"]

    if opcode is Opcode.ADD:
        await conn.sadd("tournament:queue", user)
    elif opcode is Opcode.REM:
        await conn.srem("tournament:queue", user)
    else:
        raise ValueError("unsupported opcode")
