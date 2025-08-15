import argparse
import logging
from typing import Sequence

from cfnpa.helpers import format_json_string

LOGGER = logging.getLogger("cfnpa")


def configure_logging(debug_logging, info_logging):
    ch = logging.StreamHandler()

    if debug_logging:
        LOGGER.setLevel(logging.DEBUG)
    elif info_logging:
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

        logging_group = parser.add_mutually_exclusive_group()

        parser.add_argument(
            "--pipeline",
            action="store",
            type=str,
            required=True,
            help="Path to Template Containing Pipeline",
        )
        logging_group.add_argument(
            "--debug_logging",
            action="store_true",
            help="Enables Debug Level Logging",
        )
        logging_group.add_argument(
            "--info_logging",
            action="store_true",
            help="Enables Info Level Logging.",
        )

        return parser


class ConfigMixIn(CliArgs):
    def __init__(self, cli_args: list[str]):
        CliArgs.__init__(self, cli_args)

    def __repr__(self):
        return format_json_string(
            {
                "pipeline_file": self.pipeline_file,
                "debug_logging": self.debug_logging,
                "info_logging": self.info_logging,
            }
        )

    def _get_argument_value(self, arg_name):
        return getattr(self.cli_args, arg_name)

    @property
    def pipeline_file(self):
        return self._get_argument_value("pipeline_file")

    @property
    def debug_logging(self):
        return self._get_argument_value("debug_logging")

    @property
    def info_logging(self):
        return self._get_argument_value("info_logging")
