import logging
import sys

LOGGER = logging.getLogger("cfn-pa")


def main():
    assert sys.version_info >= (3, 13)


if __name__ == "__main__":
    main()
