import asyncio
import os
from asyncio.subprocess import Process
from pathlib import Path
from typing import Optional

from rich import print

from multistage.constants import NODE_PROCESS_ULIMIT


class NodeController:
    def __init__(self) -> None:
        self.process: Optional[Process] = None

    async def start(self, program: str, args: list[str], cwd: Path):
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

    def stop(self):
        assert self.process is not None

        print("Stopping node ...")
        self.process.kill()
