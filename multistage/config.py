

from pathlib import Path
from typing import Any

from multistage import errors


class BuildConfigEntry:
    def __init__(self, name: str, go_url: str, source_url: str, destination_folder: str) -> None:
        if not name:
            raise errors.KnownError("build 'name' is required")
        if not go_url:
            raise errors.KnownError("build 'go url' is required")
        if not source_url:
            raise errors.KnownError("build 'source' is required")
        if not destination_folder:
            raise errors.KnownError("build 'destination' is required")

        self.name = name
        self.go_url = go_url
        self.source_url = source_url
        self.destination_folder = destination_folder

    @classmethod
    def new_from_dictionary(cls, data: dict[str, Any]):
        name = data.get("name") or ""
        go_url = data.get("goUrl") or ""
        source_url = data.get("sourceUrl") or ""
        destination_folder = data.get("destinationFolder") or ""

        return cls(
            name=name,
            go_url=go_url,
            source_url=source_url,
            destination_folder=destination_folder,
        )


class DriverConfig:
    def __init__(self, lanes: list["LaneConfig"]) -> None:
        lanes_names = [lane.name for lane in lanes]

        if not lanes:
            raise errors.BadConfigurationError("'lanes' are required")
        if len(lanes_names) > len(set(lanes_names)):
            raise errors.BadConfigurationError("lanes names must be unique")

        self.lanes = lanes
        self.lanes_by_name = {lane.name: lane for lane in lanes}

    @classmethod
    def new_from_dictionary(cls, data: dict[str, Any]):
        lanes_records = data.get("lanes") or []
        lanes = [LaneConfig.new_from_dictionary(record) for record in lanes_records]

        return cls(
            lanes=lanes,
        )

    def get_lanes_names(self) -> list[str]:
        return [lane.name for lane in self.lanes]

    def get_lane(self, name: str) -> "LaneConfig":
        return self.lanes_by_name[name]


class LaneConfig:
    def __init__(self, name: str, working_directory: str, stages: list["StageConfig"]) -> None:
        stages_names = [stage.name for stage in stages]

        if not name:
            raise errors.BadConfigurationError("for all lanes, 'name' is required")
        if not working_directory:
            raise errors.BadConfigurationError(f"for lane {name}, 'working directory' is required")
        if not stages:
            raise errors.BadConfigurationError(f"for lane {name}, 'stages' are required")
        if len(stages) > len(set(stages_names)):
            raise errors.BadConfigurationError("stages names must be unique")

        self.name = name
        self.working_directory = Path(working_directory).expanduser().resolve()
        self.stages = stages
        self.stages_by_name = {stage.name: stage for stage in stages}

    @classmethod
    def new_from_dictionary(cls, data: dict[str, Any]):
        name = data.get("name") or ""
        working_directory = data.get("workingDirectory") or ""
        stages_records = data.get("stages") or []
        stages = [StageConfig.new_from_dictionary(record) for record in stages_records]

        return cls(
            name=name,
            working_directory=working_directory,
            stages=stages,
        )

    def get_stages_names(self) -> list[str]:
        return [stage.name for stage in self.stages]

    def get_stages_including_and_after(self, initial_stage_name: str) -> list["StageConfig"]:
        stages_names = self.get_stages_names()
        index_of_initial_stage_name = stages_names.index(initial_stage_name)
        return self.stages[index_of_initial_stage_name:]


class StageConfig:
    def __init__(self,
                 name: str,
                 until_epoch: int,
                 node_status_url: str,
                 configuration_archive: str,
                 bin: str,
                 node_arguments: list[str],
                 with_db_lookup_extensions: bool,
                 with_indexing: bool) -> None:
        if not name:
            raise errors.BadConfigurationError("for all stages, 'name' is required")
        if not until_epoch:
            raise errors.BadConfigurationError(f"for stage {name}, 'until epoch' is required")
        if not node_status_url:
            raise errors.BadConfigurationError(f"for stage {name}, 'node status url' is required")
        if not configuration_archive:
            raise errors.BadConfigurationError(f"for stage {name}, 'configuration archive' is required")
        if not bin:
            raise errors.BadConfigurationError(f"for stage {name}, 'bin' is required")

        self.name = name
        self.until_epoch = until_epoch
        self.node_status_url = node_status_url
        self.configuration_archive = configuration_archive
        self.bin = Path(bin).expanduser().resolve()
        self.node_arguments = node_arguments
        self.with_db_lookup_extensions = with_db_lookup_extensions
        self.with_indexing = with_indexing

    @classmethod
    def new_from_dictionary(cls, data: dict[str, Any]):
        name = data.get("name") or ""
        until_epoch = data.get("untilEpoch") or 0
        node_status_url = data.get("nodeStatusUrl") or ""
        configuration_archive = data.get("configurationArchive") or ""
        bin = data.get("bin") or ""
        node_arguments = data.get("nodeArguments") or []
        with_db_lookup_extensions = data.get("withDbLookupExtensions") or False
        with_indexing = data.get("withIndexing") or False

        return cls(
            name=name,
            until_epoch=until_epoch,
            node_status_url=node_status_url,
            configuration_archive=configuration_archive,
            bin=bin,
            node_arguments=node_arguments,
            with_db_lookup_extensions=with_db_lookup_extensions,
            with_indexing=with_indexing,
        )
