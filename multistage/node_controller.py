from pathlib import Path


class NodeController:
    def __init__(self, shard: int, api_port: int) -> None:
        self.pid = 0
        self.shard = shard
        self.api_port = api_port

    async def start(self, args: list[str], cwd: Path, delay: int = 0):
        pass

    def stop(self):
        pass
