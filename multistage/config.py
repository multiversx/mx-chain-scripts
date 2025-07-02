

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
        if not lanes:
            raise errors.BadConfigurationError("'lanes' are required")

        self.lanes = lanes

    @classmethod
    def new_from_dictionary(cls, data: dict[str, Any]):
        lanes = data.get("lanes") or []

        return cls(
            lanes=lanes,
        )


class LaneConfig:
    def __init__(self, name: str, working_directory: str, stages: list["StageConfig"]) -> None:
        self.name = name
        self.working_directory = working_directory
        self.stages = stages


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
            raise errors.BadConfigurationError("'name' is required")
        if not until_epoch:
            raise errors.BadConfigurationError("'until epoch' is required")
        if not node_status_url:
            raise errors.BadConfigurationError("'node status url' is required")
        if not configuration_archive:
            raise errors.BadConfigurationError("'configuration archive' is required")
        if not bin:
            raise errors.BadConfigurationError("'bin' is required")

        self.name = name
        self.until_epoch = until_epoch
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
