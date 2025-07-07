import asyncio
from typing import Any, Coroutine, Optional

from rich import print
from rich.rule import Rule

from multistage.config import LaneConfig
from multistage.constants import (NODE_MONITORING_PERIOD,
                                  NODE_RETURN_CODE_SIGKILL,
                                  NODE_RETURN_CODE_SUCCESS)
from multistage.stage_controller import StageController


class LaneController:
    def __init__(self, config: LaneConfig, initial_stage_name: str) -> None:
        self.config = config
        self.initial_stage_name = initial_stage_name
        self.current_stage_controller: Optional[StageController] = None

    def start(self):
        try:
            asyncio.run(self._do_start())
        except KeyboardInterrupt:
            print("Processing lane interrupted.")

    async def _do_start(self):
        stages = self.config.get_stages_including_and_after(self.initial_stage_name)

        for stage in stages:
            print(Rule(f"[bold yellow]{stage.name}"))

            self.current_stage_controller = StageController(stage)

            working_directory = self.config.working_directory
            working_directory.mkdir(parents=True, exist_ok=True)

            self.current_stage_controller.configure(working_directory)

            coroutines: list[Coroutine[Any, Any, None]] = [
                self.current_stage_controller.start(working_directory),
                self.monitor_stage()
            ]

            tasks = [asyncio.create_task(item) for item in coroutines]
            await asyncio.gather(*tasks, return_exceptions=False)

            return_code = self.current_stage_controller.return_code

            if return_code == NODE_RETURN_CODE_SIGKILL:
                continue
            if return_code != NODE_RETURN_CODE_SUCCESS:
                break

    async def monitor_stage(self):
        controller = self.current_stage_controller

        assert controller is not None

        while True:
            await asyncio.sleep(NODE_MONITORING_PERIOD)

            if not controller.is_running():
                return

            if controller.should_stop():
                controller.stop()
                return
