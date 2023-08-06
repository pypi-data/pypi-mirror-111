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

import asyncio
import logging
import secrets
import time

import aioredis

from . import redis

logger: logging.Logger = logging.getLogger(__name__)

INTERVAL: int = 5
STARTING_POSITION_ID = "4HPwATDgc/ABMA"
STARTING_MATCH_ID = "cAgAAAAAAAAA"


async def run() -> None:
    try:
        while True:
            sleep_task: asyncio.Task = asyncio.create_task(asyncio.sleep(INTERVAL))
            match_task: asyncio.Task = asyncio.create_task(_match())
            await asyncio.gather(sleep_task, match_task)
    except asyncio.CancelledError:
        sleep_task.cancel()
        match_task.cancel()


async def _match() -> None:
    try:
        start: float = time.perf_counter()
        await _find_match()
        elapsed: float = time.perf_counter() - start
        if elapsed > INTERVAL:
            logger.warning(f"match took {round(elapsed, 1)}s to execute")
    except asyncio.CancelledError:
        pass


async def _find_match() -> None:
    conn: aioredis.Redis = await redis.get_connection()

    await conn.sunionstore("tournament:clone", "tournament:queue")

    while await conn.scard("tournament:clone") > 1:
        pipeline: aioredis.commands.transaction.MultiExec = conn.multi_exec()

        game_id: str = secrets.token_urlsafe(9)

        pipeline.hset(f"game:{game_id}", "position", STARTING_POSITION_ID)
        pipeline.hset(f"game:{game_id}", "match", STARTING_MATCH_ID)

        for i, player in enumerate(
            await conn.spop("tournament:clone", 2, encoding="utf-8")
        ):
            pipeline.srem("tournament:queue", player)
            pipeline.hset(f"game:{game_id}", f"player_{i}", player)
            pipeline.hset(f"session:{player}", "game_id", game_id)
            pipeline.publish(f"tournament:{player}", game_id)

        await pipeline.execute()
