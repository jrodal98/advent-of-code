#!/usr/bin/env python3
# www.jrodal.com


import unittest
import sys

from io import StringIO
from rich.console import Console
from rich.traceback import Traceback
from typing import Type


class RichTestResult(unittest.TextTestResult):
    def _exc_info_to_string(self, err, test):
        exctype, value, tb = err
        file = StringIO()
        console = Console(
            file=file, force_terminal=True
        )  # create a Console that writes to a string buffer
        traceback = Traceback.from_exception(
            exctype, value, tb, suppress=[unittest], show_locals=self.tb_locals
        )
        console.print(traceback)  # render the traceback to the console
        return file.getvalue()  # return the contents of the string buffer


class RichTestRunner(unittest.TextTestRunner):
    resultclass = RichTestResult

    def make_suite_and_run(self, test_case_cls: Type[unittest.TestCase]) -> None:
        result = self.run(unittest.makeSuite(test_case_cls))
        if not result.wasSuccessful():
            sys.exit(1)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner, tb_locals=True)
