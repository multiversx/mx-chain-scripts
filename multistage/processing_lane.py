import asyncio
import os
from pathlib import Path
from typing import Any, Coroutine, Optional

from rich import print

from multistage.config import LaneConfig, StageConfig
from multistage.node_controller import NodeController


class ProcessingLane:
    def __init__(self, config: LaneConfig, initial_stage_name: str) -> None:
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
            print("Processing lane interrupted.")

    async def _do_start(self):
        node_controller = NodeController()

        coroutines: list[Coroutine[Any, Any, None]] = [
            node_controller.start("tbd", [], Path("")),
            self.monitor_node()
        ]

        tasks = [asyncio.create_task(item) for item in coroutines]
        await asyncio.gather(*tasks, return_exceptions=False)

    async def monitor_node(self):
        loop = asyncio.get_running_loop()

        while True:
            await asyncio.sleep(1000)
