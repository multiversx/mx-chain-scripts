import json
import sys
import traceback
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from rich import print
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule

from multistage import errors
from multistage.config import DriverConfig
from multistage.processing_lane import ProcessingLane


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
    parser.add_argument("--lane", required=True, help="which lane to handle")
    parser.add_argument("--stage", required=True, help="initial stage on the lane")
    args = parser.parse_args(cli_args)

    config_path = Path(args.config).expanduser().resolve()
    config_data = json.loads(config_path.read_text())
    driver_config = DriverConfig.new_from_dictionary(config_data)
    lane_name = args.lane
    initial_stage_name = args.stage

    if lane_name not in driver_config.get_lanes_names():
        raise errors.BadConfigurationError(f"unknown lane: {lane_name}")

    lane_config = driver_config.get_lane(lane_name)

    if initial_stage_name not in lane_config.get_stages_names():
        raise errors.BadConfigurationError(f"unknown stage: {initial_stage_name}")

    print(f"[bold yellow]Lane: {lane_name}")
    print(f"[bold yellow]Initial stage: {initial_stage_name}")

    lane = ProcessingLane(lane_config, initial_stage_name)
    lane.start()


if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)
