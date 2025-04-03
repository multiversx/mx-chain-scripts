import json
import os
import shutil
import subprocess
import sys
import traceback
import urllib.request
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from rich import print
from rich.panel import Panel
from rich.rule import Rule

from multiversion import errors
from multiversion.constants import FILE_MODE_NICE


class BuildConfigEntry:
    def __init__(self, name: str, source_url: str, destination_folder: str) -> None:
        if not name:
            raise errors.KnownError("build 'name' is required")
        if not source_url:
            raise errors.KnownError("build 'source' is required")
        if not destination_folder:
            raise errors.KnownError("build 'destination' is required")

        self.name = name
        self.source_url = source_url
        self.destination_folder = destination_folder

    @classmethod
    def new_from_dictionary(cls, data: dict[str, Any]):
        name = data.get("name") or ""
        source_url = data.get("sourceUrl") or ""
        destination_folder = data.get("destinationFolder") or ""

        return cls(
            name=name,
            source_url=source_url,
            destination_folder=destination_folder,
        )


def main(cli_args: list[str] = sys.argv[1:]):
    try:
        _do_main(cli_args)
    except errors.KnownError as err:
        print(Panel(f"[red]{traceback.format_exc()}"))
        print(Panel(f"[red]{err.get_pretty()}"))
        return 1


def _do_main(cli_args: list[str]):
    parser = ArgumentParser()
    parser.add_argument("--workspace", required=True, help="path of the build workspace")
    parser.add_argument("--config", required=True, help="path of the 'build' configuration file")
    args = parser.parse_args(cli_args)

    workspace_path = Path(args.workspace).expanduser().resolve()
    workspace_path.mkdir(parents=True, exist_ok=True)

    config_path = Path(args.config).expanduser().resolve()
    config_data = json.loads(config_path.read_text())
    config_entries = [BuildConfigEntry.new_from_dictionary(item) for item in config_data]

    for entry in config_entries:
        print(Rule(f"[bold yellow]{entry.name}"))
        source_parent_folder = do_download(workspace_path, entry)
        cmd_node_folder = do_build(source_parent_folder)
        copy_artifacts(cmd_node_folder, entry)


def do_download(workspace: Path, entry: BuildConfigEntry) -> Path:
    download_folder = workspace / entry.name
    extraction_folder = workspace / entry.name
    url = entry.source_url

    print(f"Re-creating {download_folder} ...")
    shutil.rmtree(download_folder, ignore_errors=True)
    download_folder.mkdir(parents=True, exist_ok=True)

    print(f"Re-creating {extraction_folder} ...")
    shutil.rmtree(extraction_folder, ignore_errors=True)
    extraction_folder.mkdir(parents=True, exist_ok=True)

    archive_extension = url.split(".")[-1]
    download_path = download_folder / f"source.{archive_extension}"

    print(f"Downloading archive {url} to {download_path}")
    urllib.request.urlretrieve(url, download_path)

    print(f"Unpacking archive {download_path} to {extraction_folder}")
    shutil.unpack_archive(download_path, extraction_folder, format="zip")

    return extraction_folder


def do_build(source_parent_folder: Path) -> Path:
    # If has one subfolder, that one is the source code
    subfolders = [Path(item.path) for item in os.scandir(source_parent_folder) if item.is_dir()]
    source_folder = subfolders[0] if len(subfolders) == 1 else source_parent_folder

    cmd_node = source_folder / "cmd" / "node"
    go_mod = source_folder / "go.mod"

    print(f"Building {cmd_node} ...")

    return_code = subprocess.check_call(["go", "build"], cwd=cmd_node)
    if return_code != 0:
        raise errors.KnownError(f"error code = {return_code}, see output")

    copy_wasmer_libraries(go_mod, cmd_node)
    return cmd_node


def copy_wasmer_libraries(go_mod: Path, destination: Path):
    go_path_variable = os.environ.get("GOPATH", "~/go")
    go_path = Path(go_path_variable).expanduser().resolve()
    vm_go_folder_name = get_chain_vm_go_folder_name(go_mod)
    vm_go_path = go_path / "pkg" / "mod" / vm_go_folder_name
    libraries = list((vm_go_path / "wasmer").glob("*.so")) + list((vm_go_path / "wasmer2").glob("*.so"))

    for library in libraries:
        shutil.copy(library, destination)
        os.chmod(destination / library.name, FILE_MODE_NICE)


def get_chain_vm_go_folder_name(go_mod: Path) -> str:
    lines = go_mod.read_text().splitlines()
    line = [line for line in lines if "github.com/multiversx/mx-chain-vm-go" in line][0]
    parts = line.split()
    return f"{parts[0]}@{parts[1]}"


def copy_artifacts(cmd_node_folder: Path, entry: BuildConfigEntry):
    print(f"Copying artifacts to {entry.destination_folder} ...")

    libraries = list(cmd_node_folder.glob("*.so"))
    executable = cmd_node_folder / "node"
    artifacts = libraries + [executable]

    destination_folder = Path(entry.destination_folder).expanduser().resolve()
    shutil.rmtree(destination_folder, ignore_errors=True)
    destination_folder.mkdir(parents=True, exist_ok=True)

    for artifact in artifacts:
        shutil.copy(artifact, destination_folder)


if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)
