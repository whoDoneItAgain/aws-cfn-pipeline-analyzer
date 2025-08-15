import logging
import sys

from cfnpa.config import ConfigMixIn, configure_logging

LOGGER = logging.getLogger(__name__)


class Runner:
    def __init__(self, config: ConfigMixIn) -> None:
        self.config = config

    def cli(self) -> None:
        configure_logging(self.config.debug_logging, self.config.info_logging)

        LOGGER.info("test info")
        LOGGER.debug("test debug")


def main() -> None:
    try:
        config = ConfigMixIn(sys.argv[1:])
    except Exception as e:
        print(e)
        sys.exit(1)
    runner = Runner(config)
    runner.cli()


if __name__ == "__main__":
    main()
