import json
import os
import shutil
import subprocess
import sys
import traceback
import urllib.request
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, List

from rich import print
from rich.panel import Panel
from rich.rule import Rule

from multiversion import errors, platform
from multiversion.constants import FILE_MODE_EXECUTABLE


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
        do_download(workspace_path, entry)
        do_build(workspace_path, entry)


def do_download(workspace: Path, entry: BuildConfigEntry):
    download_folder = workspace / "downloads" / entry.name
    extraction_folder = get_extraction_folder(workspace, entry)
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


def get_extraction_folder(workspace: Path, entry: BuildConfigEntry):
    return workspace / "builds" / entry.name


def do_build(workspace: Path, entry: BuildConfigEntry):
    extraction_folder = get_extraction_folder(workspace, entry)
    source_folder = locate_source_folder_in_archive_extraction_folder(extraction_folder)
    cmd_node = source_folder / "cmd" / "node"
    go_mod = source_folder / "go.mod"

    print(f"Building {cmd_node} ...")

    return_code = subprocess.check_call(["go", "build"], cwd=cmd_node)
    if return_code != 0:
        raise errors.KnownError(f"error code = {return_code}, see output")

    copy_wasmer_libs(go_mod, cmd_node)
    set_rpath(cmd_node / "node")


def locate_source_folder_in_archive_extraction_folder(extraction_folder: Path) -> Path:
    # If has one subfolder, that one is the source code
    subfolders = list(extraction_folder.glob("*"))
    source_folder = subfolders[0] if len(subfolders) == 1 else extraction_folder

    # Heuristic to check if this is a valid source code folder
    assert (source_folder / "go.mod").exists(), f"This is not a valid source code folder: {source_folder}"
    return source_folder


def copy_wasmer_libs(go_mod: Path, destination: Path):
    go_path_variable = os.environ.get("GOPATH", "~/go")
    go_path = Path(go_path_variable).expanduser().resolve()
    vm_go_folder_name = get_chain_vm_go_folder_name(go_mod)
    vm_go_path = go_path / "pkg" / "mod" / vm_go_folder_name
    wasmer_path = vm_go_path / "wasmer"
    wasmer2_path = vm_go_path / "wasmer2"

    copy_libraries(wasmer_path, destination)
    copy_libraries(wasmer2_path, destination)


def get_chain_vm_go_folder_name(go_mod: Path) -> str:
    lines = go_mod.read_text().splitlines()
    line = [line for line in lines if "github.com/multiversx/mx-chain-vm-go" in line][0]
    parts = line.split()
    return f"{parts[0]}@{parts[1]}"


def copy_libraries(source: Path, destination: Path):
    libraries: List[Path] = list(source.glob("*.dylib")) + list(source.glob("*.so"))

    for library in libraries:
        print(f"Copying {library} to {destination}")
        shutil.copy(library, destination)

        # Seems to be necessary on MacOS (or, at least, was necessary in the past).
        os.chmod(destination / library.name, FILE_MODE_EXECUTABLE)


def set_rpath(cmd_path: Path):
    """
    Set the rpath of the executable to the current directory, on a best-effort basis.

    For other occurrences of this approach, see:
     - https://github.com/multiversx/mx-chain-scenario-cli-go/blob/master/.github/workflows/on_release_attach_artifacts.yml
    """

    if not platform.is_osx():
        # We're only patching the executable on macOS.
        # For Linux, we're leveraging LD_LIBRARY_PATH to resolve the libraries.
        return

    try:
        subprocess.check_call([
            "install_name_tool",
            "-add_rpath",
            "@loader_path",
            cmd_path
        ])
    except Exception as e:
        # In most cases, this isn't critical (libraries might be found among the downloaded Go packages).
        print(f"Failed to set rpath of {cmd_path}: {e}")


if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)
