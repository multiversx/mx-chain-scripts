import asyncio
import os
import shutil
from asyncio.subprocess import Process
from http import HTTPStatus
from pathlib import Path
from typing import Optional

import requests
from rich import print

from multistage.config import StageConfig
from multistage.constants import NODE_PROCESS_ULIMIT
from multistage.shared import fetch_archive


class StageController:
    def __init__(self, config: StageConfig) -> None:
        self.config = config
        self.process: Optional[Process] = None
        self.return_code = -1

    def configure(self, working_directory: Path):
        config_directory = working_directory / "config"
        shutil.rmtree(config_directory, ignore_errors=True)
        fetch_archive(self.config.configuration_archive, config_directory)

    async def start(self, working_directory: Path):
        program = self.config.bin / "node"
        args = self.config.node_arguments

        print(f"Starting node in {working_directory} ...")
        print(args)

        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = str(working_directory)

        self.process = await asyncio.create_subprocess_exec(
            program,
            *args,
            stdout=asyncio.subprocess.DEVNULL,
            cwd=working_directory,
            limit=NODE_PROCESS_ULIMIT,
            env=env,
        )

        return_code = await self.process.wait()
        print(f"Node stopped, with return code = {return_code}. See node's logs.")

        self.process = None
        self.return_code = return_code

    def stop(self):
        assert self.process is not None

        print("Stopping node ...")
        self.process.kill()
        self.process = None

    def is_running(self) -> bool:
        return self.process is not None

    def should_stop(self) -> bool:
        epoch = self.get_current_epoch()
        return epoch > self.config.until_epoch

    def get_current_epoch(self) -> int:
        status_url = self.config.node_status_url

        try:
            response = requests.get(status_url)

            if response.status_code != HTTPStatus.OK:
                return 0

            data = response.json().get("data", {})
            metrics = data.get("metrics", {})
            epoch = int(metrics.get("erd_epoch_number", 0))
            block_nonce = int(metrics.get("erd_nonce", 0))

            print(f"Epoch = {epoch}, block = {block_nonce}")

            return epoch
        except Exception as error:
            print(f"[red]Error:[/red] {error}")
            return 0
