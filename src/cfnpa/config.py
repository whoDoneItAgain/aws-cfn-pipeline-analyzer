import argparse
import logging
from typing import Sequence

from cfnpa.helpers import format_json_string

LOGGER = logging.getLogger("cfnpa")


def configure_logging(debug, info):
    ch = logging.StreamHandler()

    if debug:
        LOGGER.setLevel(logging.DEBUG)
    elif info:
        LOGGER.setLevel(logging.INFO)
    else:
        LOGGER.setLevel(logging.WARNING)
    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(log_formatter)

    # make sure all other log handlers are removed before adding it back
    for handler in LOGGER.handlers:
        LOGGER.removeHandler(handler)
    LOGGER.addHandler(ch)


class CliArgs:
    """Base Args class"""

    def __init__(self, cli_args: Sequence[str] | None):
        self.parser = self.create_parser()
        self.cli_args = self.parser.parse_args(cli_args or [])

    def create_parser(self):
        parser = argparse.ArgumentParser(description="Cloudformation Pipeline Analyzer")

        standard = parser.add_argument_group("Standard")
        advanced = parser.add_argument_group("Advanced / Debugging")

        logging_group = advanced.add_mutually_exclusive_group()

        standard.add_argument(
            "-P",
            "--pipeline",
            action="store",
            type=str,
            required=True,
            help="Path to Template Containing Pipeline",
        )
        logging_group.add_argument(
            "-I",
            "--info",
            action="store_true",
            help="Enables Info Level Logging.",
        )
        logging_group.add_argument(
            "-D",
            "--debug",
            action="store_true",
            help="Enables Debug Level Logging",
        )

        return parser


class ConfigMixIn(CliArgs):
    def __init__(self, cli_args: list[str]):
        CliArgs.__init__(self, cli_args)

    def __repr__(self):
        return format_json_string(
            {
                "pipeline": self.pipeline,
                "debug": self.debug,
                "info": self.info,
            }
        )

    def _get_argument_value(self, arg_name):
        return getattr(self.cli_args, arg_name)

    @property
    def pipeline(self):
        return self._get_argument_value("pipeline")

    @property
    def debug(self):
        return self._get_argument_value("debug")

    @property
    def info(self):
        return self._get_argument_value("info")
