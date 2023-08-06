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
import logging
from typing import Optional

from . import config

logger: logging.Logger = logging.getLogger(__name__)

_redis: Optional[aioredis.Redis] = None


async def open() -> None:
    global _redis

    _redis = await aioredis.create_redis_pool(config.REDIS)
    logger.info(f"redis connected on {config.REDIS}")


async def get_connection() -> aioredis.Redis:
    global _redis

    if _redis is None:
        raise RuntimeError("no redis connection")

    return _redis


async def close() -> None:
    global _redis

    if _redis is not None:
        _redis.close()
        await _redis.wait_closed()
        logger.info("redis connection closed")
