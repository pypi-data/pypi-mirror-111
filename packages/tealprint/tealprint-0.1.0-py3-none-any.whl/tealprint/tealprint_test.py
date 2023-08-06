from __future__ import print_function

import pytest
from mockito import spy2, unstub, verify, verifyZeroInteractions

from .tealprint import TealLevel, TealPrint


@pytest.mark.parametrize(
    "name,level,function_tuple",
    [
        (
            "Prints nothing when level is none",
            TealLevel.none,
            [
                (TealPrint.error, False),
                (TealPrint.warning, False),
                (TealPrint.info, False),
                (TealPrint.verbose, False),
                (TealPrint.debug, False),
            ],
        ),
        (
            "Prints error when level is error",
            TealLevel.error,
            [
                (TealPrint.error, True),
                (TealPrint.warning, False),
                (TealPrint.info, False),
                (TealPrint.verbose, False),
                (TealPrint.debug, False),
            ],
        ),
        (
            "Prints warning+error when level is warning",
            TealLevel.warning,
            [
                (TealPrint.error, True),
                (TealPrint.warning, True),
                (TealPrint.info, False),
                (TealPrint.verbose, False),
                (TealPrint.debug, False),
            ],
        ),
        (
            "Prints info+warning+error when level is info",
            TealLevel.info,
            [
                (TealPrint.error, True),
                (TealPrint.warning, True),
                (TealPrint.info, True),
                (TealPrint.verbose, False),
                (TealPrint.debug, False),
            ],
        ),
        (
            "Prints verbose+info+warning.error when level is verbose",
            TealLevel.verbose,
            [
                (TealPrint.error, True),
                (TealPrint.warning, True),
                (TealPrint.info, True),
                (TealPrint.verbose, True),
                (TealPrint.debug, False),
            ],
        ),
        (
            "Prints everything when level is debug",
            TealLevel.debug,
            [
                (TealPrint.error, True),
                (TealPrint.warning, True),
                (TealPrint.info, True),
                (TealPrint.verbose, True),
                (TealPrint.debug, True),
            ],
        ),
    ],
)
def test_print_level(name: str, level: TealLevel, function_tuple):
    print(name)

    TealPrint.level = level

    for function, expected in function_tuple:
        spy2(TealPrint._print)

        function("message")

        if expected:
            verify(TealPrint, atleast=1)._print(...)
        else:
            verifyZeroInteractions()

        unstub()
