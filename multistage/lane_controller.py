import asyncio
from typing import Any, Coroutine, Optional

from rich import print
from rich.rule import Rule

from multistage.config import LaneConfig, StageConfig
from multistage.constants import (NODE_MONITORING_PERIOD,
                                  NODE_RETURN_CODE_SUCCESS)
from multistage.node_controller import NodeController


class LaneController:
    def __init__(self, config: LaneConfig, initial_stage_name: str) -> None:
        self.config = config
        self.initial_stage_name = initial_stage_name
        self.current_stage: Optional[StageConfig] = None
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
        stages = self.config.get_stages_including_and_after(self.initial_stage_name)

        for stage in stages:
            print(Rule(f"[bold yellow]{stage.name}"))

            self.current_stage = stage
            self.current_node_controller = NodeController()

            node_program = str(stage.bin / "node")
            node_arguments = stage.node_arguments
            cwd = self.config.working_directory

            cwd.mkdir(parents=True, exist_ok=True)

            coroutines: list[Coroutine[Any, Any, None]] = [
                self.current_node_controller.start(node_program, node_arguments, cwd),
                self.monitor_node()
            ]

            tasks = [asyncio.create_task(item) for item in coroutines]
            await asyncio.gather(*tasks, return_exceptions=False)

            return_code = self.current_node_controller.return_code
            if return_code != NODE_RETURN_CODE_SUCCESS:
                break

    async def monitor_node(self):
        assert self.current_stage is not None
        assert self.current_node_controller is not None

        print("Node status URL:", self.current_stage.node_status_url)

        while True:
            await asyncio.sleep(NODE_MONITORING_PERIOD)

            if not self.current_node_controller.is_running():
                return
