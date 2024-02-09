
import pytest
import allure
from allure_commons.types import AttachmentType

from os import path

import scripts.ASProject as ASProject

def test_ASVersion(project):
    version = ASProject.ASProject._version(project)
    assert '4.12.2.93' == version

def test_ASVersion_sp(project_sp):
    version = ASProject.ASProject._version(project_sp)
    assert '4.12.4.107' == version

def test_ASWorkingVersion(project):
    version = ASProject.ASProject._workingVersion(project)
    assert '4.12' == version

def test_ArmExport(tmp_path, project, source_library_c, config1, config_arm):
    as_project = ASProject.ASProject(project)
    as_project.exportLibrary("Test_lib", tmp_path)
    
    assert path.exists(tmp_path / "Test_lib")
    lib = tmp_path / "Test_lib" / "V2.30.1"
    assert path.exists(lib / "SG3")
    assert path.exists(lib / "SG4")
    assert path.exists(lib / "SGC")
    assert path.exists(lib / "Binary.lby")
    assert path.exists(lib / "Test_Lib.fun")
    assert path.exists(lib / "Test_Lib.typ")
    assert path.exists(lib / "Test_Lib.var")
    assert path.exists(lib / "SG4" / "Test_lib.br")
    assert path.exists(lib / "SG4" / "Test_lib.h")
    assert path.exists(lib / "SG4" / "libTest_lib.a")
    assert path.exists(lib / "SG4" / "ARM" / "Test_lib.br")
    assert path.exists(lib / "SG4" / "ARM" / "libTest_lib.a")

def test_SG4Export(tmp_path, project, source_library_c, config1):
    as_project = ASProject.ASProject(project)
    as_project.exportLibrary("Test_lib", tmp_path)
    
    assert path.exists(tmp_path / "Test_lib")
    lib = tmp_path / "Test_lib" / "V2.30.1"
    assert path.exists(lib / "SG3")
    assert path.exists(lib / "SG4")
    assert path.exists(lib / "SGC")
    assert path.exists(lib / "Binary.lby")
    assert path.exists(lib / "Test_Lib.fun")
    assert path.exists(lib / "Test_Lib.typ")
    assert path.exists(lib / "Test_Lib.var")
    assert path.exists(lib / "SG4" / "Test_lib.br")
    assert path.exists(lib / "SG4" / "Test_lib.h")
    assert path.exists(lib / "SG4" / "libTest_lib.a")
    