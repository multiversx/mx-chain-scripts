import asyncio
import os
from pathlib import Path
from typing import Any, Coroutine

from multistage.config import StageConfig


class ProcessingLane:
    def __init__(self, shard: int, stages: list[StageConfig]) -> None:
        self.shard = shard
        self.stages = stages


def start():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(do_start())
        loop.close()
        asyncio.set_event_loop(asyncio.new_event_loop())
    except KeyboardInterrupt:
        pass


async def do_start():
    coroutines: list[Coroutine[Any, Any, None]] = [
        run(
            ["TBD", "TBD"],
            cwd=Path("."),
            delay=1000,
        ),
        monitor_network()
    ]

    tasks = [asyncio.create_task(item) for item in coroutines]
    await asyncio.gather(*tasks)


async def monitor_network():
    loop = asyncio.get_running_loop()

    while True:
        await asyncio.sleep(1000)


async def run(args: list[str], cwd: Path, delay: int = 0):
    await asyncio.sleep(delay)

    print(f"Starting process {args} in folder {cwd}")

    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = str(cwd)

    process = await asyncio.create_subprocess_exec(
        *args,
        cwd=cwd,
        limit=1024 * 512,
        env=env,
    )

    pid = process.pid
    return_code = await process.wait()
    print(f"Proces [{pid}] stopped. Return code: {return_code}.")
