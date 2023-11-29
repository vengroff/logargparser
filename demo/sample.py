import logging
from logargparser import LoggingArgumentParser

logger = logging.getLogger(__name__)


def main():
    # Instead of the normal `parser = argparse.ArgumentParser.
    parser = LoggingArgumentParser(logger)

    # Add as many other arguments as you want.
    parser.add_argument('-o', "--output")

    args = parser.parse_args()

    logger.info("The logger was set up for us based on --log and/or --logfile command line args.")

    if args.output is not None:
        # Do something....
        pass


if __name__ == "__main__":
    main()