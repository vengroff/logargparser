import unittest
import logging
from pathlib import Path
from shutil import rmtree
from logargparser import LoggingArgumentParser


class LogTestCase(unittest.TestCase):
    """Test parsing --log and --logfile."""

    def setUp(self) -> None:
        """Set up the parser."""
        self.logger = logging.getLogger("test")
        self.parser = LoggingArgumentParser(self.logger)

    def test_parse_log(self) -> None:
        """Set the log level."""
        args = self.parser.parse_args(["--log", "INFO"])
        self.assertEqual("INFO", args.log)  # add assertion here

    def test_parse_log_default(self) -> None:
        """Default is WARNING."""
        args = self.parser.parse_args([])
        self.assertEqual("WARNING", args.log)  # add assertion here


class LogfileTestCase(unittest.TestCase):
    """Test directing the log to a file."""


    @classmethod
    def setUpClass(cls) -> None:
        """Global set up once."""
        cls.output_dir = Path(__file__).parent / "_test_artifacts"
        rmtree(cls.output_dir, ignore_errors=True)
        cls.output_dir.mkdir(parents=True)

    def setUp(self) -> None:
        """Set up before each test."""
        # Get rid of all the existing handlers before we
        # run each test.
        logger = logging.getLogger()
        for handler in logger.handlers:
            handler.close()
            logger.removeHandler(handler)

    def test_output_file(self):
        logger = logging.getLogger("test_output_file")
        parser = LoggingArgumentParser(logger)

        log_path = self.output_dir / "output.log"

        parser.parse_args(["--logfile", str(log_path)])

        logger.debug("This is for debugging.")
        logger.info("This is some info.")
        logger.warning("This is a warning.")

        # Make sure just the warning got there.
        with open(log_path, "r") as f:
            log_text = f.read()
            self.assertEqual("WARNING:test_output_file:This is a warning.\n", log_text)

    def test_output_file_info(self):
        logger = logging.getLogger("test_output_file_info")
        parser = LoggingArgumentParser(logger)

        log_path = self.output_dir / "output-info.log"

        parser.parse_args(["--log", "INFO", "--logfile", str(log_path)])

        logger.debug("This is for debugging.")
        logger.info("This is some info.")
        logger.warning("This is a warning.")

        # Make sure just the warning got there.
        with open(log_path, "r") as f:
            log_text = f.read()
            self.assertEqual(
                "INFO:test_output_file_info:This is some info.\nWARNING:test_output_file_info:This is a warning.\n",
                log_text,
            )


if __name__ == "__main__":
    unittest.main()
