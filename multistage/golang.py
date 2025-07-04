import os
import subprocess
from pathlib import Path

from rich import print

from multistage import errors
from multistage.shared import fetch_archive


class BuildEnvironment:
    def __init__(self, system_path: str, go_path: str, go_cache: str, go_root: str) -> None:
        self.system_path = system_path
        self.go_path = go_path
        self.go_cache = go_cache
        self.go_root = go_root

    def to_dictionary(self) -> dict[str, str]:
        return {
            "PATH": self.system_path,
            "GOPATH": self.go_path,
            "GOCACHE": self.go_cache,
            "GOROOT": self.go_root,
        }


def acquire_environment(workspace: Path, label: str) -> BuildEnvironment:
    directory = get_environment_directory(workspace, label)
    current_system_path = os.environ.get("PATH", "")

    return BuildEnvironment(
        system_path=f"{directory / 'bin'}:{current_system_path}",
        go_path=str(directory / "gopath"),
        go_cache=str(directory / "gocache"),
        go_root=str(directory),
    )


def get_environment_directory(workspace: Path, label: str) -> Path:
    return workspace / f"go_{label}"


def install_go(workspace: Path, download_url: str, environment_label: str):
    environment_directory = get_environment_directory(workspace, environment_label)

    if environment_directory.exists():
        print(f"Go already installed in {environment_directory} ({environment_label}).")
        return

    fetch_archive(download_url, environment_directory)

    print(f"Creating go environment directories ...")
    (environment_directory / "gopath").mkdir()
    (environment_directory / "gocache").mkdir()


def build(source_code: Path, environment: BuildEnvironment):
    print(f"Building {source_code} ...")

    return_code = subprocess.call(["go", "build"], cwd=source_code, env=environment.to_dictionary())
    if return_code != 0:
        raise errors.KnownError(f"error code = {return_code}, see output")
