import pytest

from aiojobs._scheduler import Scheduler
from aiojobs import create_scheduler


PARAMS = dict(close_timeout=1.0, limit=100, exception_handler=None)


@pytest.fixture
def scheduler(loop):
    ret = Scheduler(loop=loop, **PARAMS)
    yield ret
    loop.run_until_complete(ret.close())


@pytest.fixture
def make_scheduler(loop):
    schedulers = []

    async def maker(**kwargs):
        ret = await(create_scheduler(**kwargs))
        schedulers.append(ret)
        return ret

    yield maker

    for scheduler in schedulers:
        loop.run_until_complete(scheduler.close())
