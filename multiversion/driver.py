import sys
import traceback
from argparse import ArgumentParser

from rich import print
from rich.panel import Panel

from multiversion import errors


def main(cli_args: list[str] = sys.argv[1:]):
    try:
        _do_main(cli_args)
    except errors.KnownError as err:
        print(Panel(f"[red]{traceback.format_exc()}"))
        print(Panel(f"[red]{err.get_pretty()}"))
        return 1


def _do_main(cli_args: list[str]):
    parser = ArgumentParser()
    args = parser.parse_args(cli_args)


if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)

