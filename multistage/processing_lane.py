from multistage.config import StageConfig


class ProcessingLane:
    def __init__(self, shard: int, stages: list[StageConfig]) -> None:
        self.shard = shard
        self.stages = stages
