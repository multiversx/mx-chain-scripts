import asyncio
import os
from asyncio.subprocess import Process
from pathlib import Path
from typing import Optional

from rich import print

from multistage.config import StageConfig
from multistage.constants import NODE_PROCESS_ULIMIT


class StageController:
    def __init__(self, config: StageConfig) -> None:
        self.config = config
        self.process: Optional[Process] = None
        self.return_code = -1

    def configure(self):
        # configurationArchive
        # "withDbLookupExtensions": true,
        # "withIndexing": false
        pass

    async def start(self, cwd: Path):
        program = self.config.bin / "node"
        args = self.config.node_arguments

        print(f"Starting node ...")
        print("args:", args)
        print("cwd:", cwd)

        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = str(cwd)

        self.process = await asyncio.create_subprocess_exec(
            program,
            *args,
            cwd=cwd,
            limit=NODE_PROCESS_ULIMIT,
            env=env,
        )

        return_code = await self.process.wait()
        print(f"Proces [{self.process.pid}] stopped. Return code: {return_code}.")

        self.process = None
        self.return_code = return_code

    def stop(self):
        assert self.process is not None

        print("Stopping node ...")
        self.process.kill()
        self.process = None

    def is_running(self) -> bool:
        return self.process is not None

    def get_current_epoch(self) -> int:
        return 42
