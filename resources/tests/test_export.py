
import pytest
import allure
from allure_commons.types import AttachmentType

from os import path
import xml.etree.ElementTree as ET

import scripts.Export as Export
import scripts.ASProject as ASProject

@pytest.mark.parametrize("tasks,libraries", [([], ['sys_lib']), ([], ['sys_lib', 'runtime']), (['Infrastructure.Backup.BackupMgr.prg', 'Infrastructure.File.FileMgr.prg'], ['sys_lib', 'runtime'])])
@allure.title("Test software deployment (tasks: {tasks}, libraries {libraries})")
def test_copySwDeployment(export, config1, tasks, libraries):
    Export.copySwDeployment(export, tasks, libraries)

    found_tasks = []
    found_libs = []
    cpu = ET.parse(export / "Config1" / "PC" / "Cpu.sw")
    ET.register_namespace('', 'http://br-automation.co.at/AS/SwConfiguration')
    ns = '{http://br-automation.co.at/AS/SwConfiguration}'
    for child in cpu.getroot():
        if (child.tag == ns + 'TaskClass'):
            for task in child.findall(ns + 'Task'):
                found_tasks.append(task.attrib['Source'])
        elif (child.tag == ns + 'Libraries'):
            for lib in child.findall(ns + 'LibraryObject'):
                found_libs.append(lib.attrib['Name'])

    print(f'tasks = {found_tasks}')
    print(f'libraries = {found_libs}')

    assert sorted(found_tasks) == sorted(tasks)
    assert sorted(found_libs) == sorted(libraries)

@pytest.mark.parametrize("fileDevices", [([]), (['mappAlarmXFiles', 'mappDataFiles'])])
@allure.title("Test file device export (fileDevices: {fileDevices})")
def test_copyFileDevices(export, config1, fileDevices): 
    Export.copyFileDevices(export, fileDevices)

    actual = []
    cpu = ET.parse(export / "Config1" / "Hardware.hw")
    ET.register_namespace('', 'http://br-automation.co.at/AS/Hardware')
    ns = '{http://br-automation.co.at/AS/Hardware}'
    for module in cpu.getroot().findall(ns + 'Module'):
        for parameter in module.findall(ns + 'Parameter'):
            if parameter.attrib['ID'].startswith('FileDeviceName'):
                actual.append(parameter.attrib['Value'])
    
    print(actual)
    assert sorted(actual) == sorted(fileDevices)

def test_enableOpcUa(export, config1):
    (export / "Config1").mkdir()
    hardware = export / "Config1" / "Hardware.hw"
    hardware.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio Version=4.12.2.93 FileVersion="4.9"?>
<Hardware xmlns="http://br-automation.co.at/AS/Hardware">
  <Module Name="PC" Type="PC_any" Version="1.1.1.0" OrderNumber="PC">
    <Parameter ID="ConfigurationID" Value="NewEmptySim_Config1" />
    <Parameter ID="Cyclic8Stack" Value="20480" />
  </Module>
</Hardware>''')
    Export.enableOpcUa(export)
    expected = [('ActivateOpcUa', '1'), ('OpcUaActivateAuditEvents', '1'), ('OpcUa_Security_AdminRole', 'Administrators')]
    actual = []
    cpu = ET.parse(export / "Config1" / "Hardware.hw")
    ET.register_namespace('', 'http://br-automation.co.at/AS/Hardware')
    ns = '{http://br-automation.co.at/AS/Hardware}'
    for module in cpu.getroot().findall(ns + 'Module'):
        for parameter in module.findall(ns + 'Parameter'):
            if parameter.attrib['ID'].startswith('ActivateOpcUa'):
                actual.append((parameter.attrib['ID'], parameter.attrib['Value']))
            elif parameter.attrib['ID'].startswith('OpcUaActivateAuditEvents'):
                actual.append((parameter.attrib['ID'], parameter.attrib['Value']))
            elif parameter.attrib['ID'].startswith('OpcUa_Security_AdminRole'):
                actual.append((parameter.attrib['ID'], parameter.attrib['Value']))
    print(actual)
    assert sorted(actual) == sorted(expected)

def test_set_user_partition_size(export, config1):
    (export / "Config1").mkdir()
    hardware = export / "Config1" / "Hardware.hw"
    hardware.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio Version=4.12.2.93 FileVersion="4.9"?>
<Hardware xmlns="http://br-automation.co.at/AS/Hardware">
  <Module Name="PC" Type="PC_any" Version="1.1.1.0" OrderNumber="PC">
    <Parameter ID="ConfigurationID" Value="NewEmptySim_Config1" />
    <Parameter ID="Cyclic8Stack" Value="20480" />
  </Module>
</Hardware>''')
    
    Export.setUserPartitionSize(export)
    expected = ['UserPartitionSize']
    actual = []
    cpu = ET.parse(export / "Config1" / "Hardware.hw")
    ET.register_namespace('', 'http://br-automation.co.at/AS/Hardware')
    ns = '{http://br-automation.co.at/AS/Hardware}'
    for module in cpu.getroot().findall(ns + 'Module'):
        for parameter in module.findall(ns + 'Parameter'):
            if parameter.attrib['ID'].startswith('UserPartitionSize'):
                actual.append(parameter.attrib['ID'])

    print(actual)
    assert sorted(actual) == sorted(expected)

def test_clearAuthentication(config1, mappViewConfig):
    Export.physicalDir = ''
    Export.clearAuthentication(config1)
    cpu = ET.parse(mappViewConfig / "Config.mappviewcfg")
    for element in cpu.getroot().findall('Element'):
        for group in element.findall('Group'):
            if (group.attrib['ID'] == 'Server'):
                for selector in group.findall('Selector'):
                    if selector.attrib['ID'] == 'AuthenticationMode':
                        pytest.fail('authentication not cleared')

@pytest.mark.skip(reason="not complete yet")
def test_compileLibraries(export, project, source_library_c):
    Export.physicalDir = ''
    project = ASProject.ASProject(project)
    exports = {'compileLibraries': ['Test_lib']}
    Export.standardExport(exports, export, project, [], [])

@allure.issue("GQXS-124")
def test_non_cpu_modules(config_x20):
    Export.physicalDir = config_x20
    Export.enableOpcUa(config_x20)
    expected = [('ActivateOpcUa', '1'), ('OpcUaActivateAuditEvents', '1'), ('OpcUa_Security_AdminRole', 'Administrators')]
    actual = []
    cpu = ET.parse(config_x20 / "Hardware.hw")
    ET.register_namespace('', 'http://br-automation.co.at/AS/Hardware')
    ns = '{http://br-automation.co.at/AS/Hardware}'
    for module in cpu.getroot().findall(ns + 'Module'):
        for parameter in module.findall(ns + 'Parameter'):
            if parameter.attrib['ID'].startswith('ActivateOpcUa'):
                actual.append((parameter.attrib['ID'], parameter.attrib['Value']))
            elif parameter.attrib['ID'].startswith('OpcUaActivateAuditEvents'):
                actual.append((parameter.attrib['ID'], parameter.attrib['Value']))
            elif parameter.attrib['ID'].startswith('OpcUa_Security_AdminRole'):
                actual.append((parameter.attrib['ID'], parameter.attrib['Value']))
    print(actual)
    assert sorted(actual) == sorted(expected)