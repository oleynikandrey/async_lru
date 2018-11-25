import asyncio

import pytest

from async_lru import alru_cache

pytestmark = pytest.mark.asyncio


async def test_expires_in(check_lru, loop):
    @alru_cache(loop=loop, expires_in=1)
    async def coro(val):
        return val

    inputs = [1, 1, 1]
    coros = [coro(v) for v in inputs]
    ret = await asyncio.gather(*coros, loop=loop)
    assert ret == inputs
    check_lru(coro, hits=2, misses=1, cache=1, tasks=0)

    await asyncio.sleep(1)

    inputs = [1, 1]
    coros = [coro(v) for v in inputs]
    ret = await asyncio.gather(*coros, loop=loop)
    assert ret == inputs

    check_lru(coro, hits=3, misses=2, cache=1, tasks=0)
