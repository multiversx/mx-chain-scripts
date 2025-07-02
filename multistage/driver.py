import json
import sys
import traceback
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from rich import print
from rich.panel import Panel
from rich.rule import Rule

from multistage import errors
from multistage.config import DriverConfig


def main(cli_args: list[str] = sys.argv[1:]):
    try:
        _do_main(cli_args)
    except errors.KnownError as err:
        print(Panel(f"[red]{traceback.format_exc()}"))
        print(Panel(f"[red]{err.get_pretty()}"))
        return 1


def _do_main(cli_args: list[str]):
    parser = ArgumentParser()
    parser.add_argument("--config", required=True, help="path of the 'driver' configuration file")
    args = parser.parse_args(cli_args)

    config_path = Path(args.config).expanduser().resolve()
    config_data = json.loads(config_path.read_text())
    driver_config = DriverConfig.new_from_dictionary(config_data)

    for lane in driver_config.lanes:
        print(Rule(f"[bold yellow]{lane.name}"))

        for stage in lane.stages:
            print(Rule(f"[bold yellow]{stage.name}"))


if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)
