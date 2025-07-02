import os
import shutil
import subprocess
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from rich import print

from multistage import errors


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
        system_path=f"{directory / 'go' / 'bin'}:{current_system_path}",
        go_path=str(directory / "gopath"),
        go_cache=str(directory / "gocache"),
        go_root=str(directory / "go"),
    )


def get_environment_directory(workspace: Path, label: str) -> Path:
    return workspace / f"go_{label}"


def install_go(workspace: Path, download_url: str, environment_label: str):
    download_url_parsed = urlparse(download_url)
    download_url_path = download_url_parsed.path
    download_to_path = workspace / Path(download_url_path).name
    environment_directory = get_environment_directory(workspace, environment_label)

    if environment_directory.exists():
        print(f"Go already installed in {environment_directory} ({environment_label}).")
        return

    print(f"Downloading {download_url} to {download_to_path} ...")
    urllib.request.urlretrieve(download_url, download_to_path)

    print(f"Extracting {environment_directory} ...")
    shutil.rmtree(environment_directory, ignore_errors=True)
    shutil.unpack_archive(download_to_path, environment_directory)

    print(f"Creating go environment directories ...")
    (environment_directory / "gopath").mkdir()
    (environment_directory / "gocache").mkdir()


def build(source_code: Path, environment: BuildEnvironment):
    print(f"Building {source_code} ...")

    return_code = subprocess.check_call(["go", "build"], cwd=source_code, env=environment.to_dictionary())
    if return_code != 0:
        raise errors.KnownError(f"error code = {return_code}, see output")
