"""
Utilities for processes and threads.
"""

import asyncio
import functools
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

PROCESS_POOL = None
THREAD_POOL = None


def init_pools():
    global PROCESS_POOL, THREAD_POOL
    PROCESS_POOL = ProcessPoolExecutor(max_workers=2)
    THREAD_POOL = ThreadPoolExecutor(max_workers=4)


def shutdown_pools():
    global PROCESS_POOL, THREAD_POOL
    if PROCESS_POOL:
        PROCESS_POOL.shutdown(wait=False)
    if THREAD_POOL:
        THREAD_POOL.shutdown(wait=False)


async def run_in_process(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    pfunc = functools.partial(func, *args, **kwargs)
    return await loop.run_in_executor(PROCESS_POOL, pfunc)


async def run_in_thread(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    tfunc = functools.partial(func, *args, **kwargs)
    return await loop.run_in_executor(THREAD_POOL, tfunc)
