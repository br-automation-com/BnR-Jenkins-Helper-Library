
import pytest
import allure
from allure_commons.types import AttachmentType

from os import path

import scripts.AsProjectCompile as ASProjectCompile

@pytest.mark.parametrize("buildResult", [(['Logical\\Libraries\\Package.pkg: (MpTweet) warning 9233:Additional directory "MpTweet" found, which is not part of the project.'])])
def test_PrintWarnings(capsys, buildResult):
    ASProjectCompile.PrintErrorsAndWarnings(buildResult)
    out, sys = capsys.readouterr()
    print(out)
    assert 'warning' in out

@pytest.mark.parametrize("buildResult", [(['Logical\\Libraries\\Package.pkg: (MpTweet) error 9233:Additional directory "MpTweet" found, which is not part of the project.'])])
def test_PrintErrors(capsys, buildResult):
    ASProjectCompile.PrintErrorsAndWarnings(buildResult)
    out, sys = capsys.readouterr()
    print(out)
    assert 'error' in out

@pytest.mark.parametrize("buildResult", [(['Logical\\Libraries\\Package.pkg: (MpTweet) :Additional directory "MpTweet" found, which is not part of the project.'])])
def test_PrintNoWarningsNoErrors(capsys, buildResult):
    ASProjectCompile.PrintErrorsAndWarnings(buildResult)
    out, sys = capsys.readouterr()
    assert '' == out
