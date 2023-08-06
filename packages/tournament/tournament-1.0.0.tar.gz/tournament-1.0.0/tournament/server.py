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
import signal
import types
from typing import Awaitable

from . import matchmaker
from . import redis
from . import queue

logger: logging.Logger = logging.getLogger(__name__)


async def serve():
    shutdown: asyncio.Future = asyncio.get_running_loop().create_future()
    _register_signal_callbacks(shutdown)

    await redis.open()

    queue_task: asyncio.Task = asyncio.create_task(queue.run())
    matchmaker_task: asyncio.Task = asyncio.create_task(matchmaker.run())
    tasks: Awaitable = asyncio.gather(queue_task, matchmaker_task)

    await shutdown

    queue_task.cancel()
    matchmaker_task.cancel()
    await tasks

    await redis.close()


def _register_signal_callbacks(shutdown: asyncio.Future):
    try:
        for s in [signal.SIGINT, signal.SIGTERM]:
            asyncio.get_running_loop().add_signal_handler(s, shutdown.set_result, None)
    except NotImplementedError:
        logger.warning("loop.add_signal_handler not supported, using workaround")
        _signal_workaround(shutdown)


def _signal_workaround(shutdown: asyncio.Future) -> None:
    """Workaround signal issues on Windows

    https://github.com/python/asyncio/issues/191
    https://github.com/python/asyncio/issues/407
    """

    async def wakeup() -> None:
        while not shutdown.done():
            await asyncio.sleep(0.1)

    def signint_handler(signalnum: int, frame: types.FrameType):
        shutdown.set_result(None)

    signal.signal(signal.SIGINT, signint_handler)
    asyncio.get_running_loop().create_task(wakeup())
