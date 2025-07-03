import asyncio
import os
from pathlib import Path
from typing import Any, Coroutine, Optional

from multistage.config import LaneConfig, StageConfig
from multistage.node_controller import NodeController


class ProcessingLane:
    def __init__(self, config: LaneConfig) -> None:
        self.config = config
        self.current_stage_index = 0
        self.current_node_controller: Optional[NodeController] = None

    def start(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._do_start())
            loop.close()
            asyncio.set_event_loop(asyncio.new_event_loop())
        except KeyboardInterrupt:
            print("Processing lange interrupted.")

    async def _do_start(self):
        # get

        coroutines: list[Coroutine[Any, Any, None]] = [
            run(
                args=["TBD", "TBD"],
                cwd=Path("."),
            ),
            monitor_network()
        ]

        tasks = [asyncio.create_task(item) for item in coroutines]
        await asyncio.gather(*tasks)


async def monitor_network():
    loop = asyncio.get_running_loop()

    while True:
        await asyncio.sleep(1000)


async def run(args: list[str], cwd: Path):
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
