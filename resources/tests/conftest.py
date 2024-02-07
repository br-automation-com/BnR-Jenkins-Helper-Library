import pytest

import allure
from allure_commons.types import AttachmentType

from os import path
import xml.etree.ElementTree as ET

import scripts.Export as Export

def make_lib(libraries, name):
    lib = libraries / name
    lib.mkdir()
    sg3 = lib / "SG3"
    sg3.mkdir()
    header = sg3 / (name + '.h')
    header.write_text('''/****************************************************************************/
/*      Automation Studio                                                   */
/*  Copyright Bernecker&Rainer 1998-1999                                    */
/****************************************************************************/
/* This library does not contain C code */''')
    sg4 = lib / "SG4"
    sg4.mkdir()
    header = sg4 / (name + '.h')
    header.write_text('''/****************************************************************************/
/*      Automation Studio                                                   */
/*  Copyright Bernecker&Rainer 1998-1999                                    */
/****************************************************************************/
/* This library does not contain C code */''')

    binary = lib / 'binary.lby'
    binary.write_text(f'''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<Library SubType="binary" Description="This library contains function interfaces for IEC 61131-3 operator functions. For the most part, these are mathematical and logical functions." xmlns="http://br-automation.co.at/AS/Library">
  <Files>
    <File>{name}.fun</File>
    <File>{name}.typ</File>
    <File>{name}.var</File>
  </Files>
</Library>''')
    fun = lib / f'{name}.fun'
    fun.write_text('''{REDUND_OK} FUNCTION SIZEOF : UDINT 		(*determines the size of a variable in bytes*)
	VAR_INPUT
		in	:ANY;				(*input value*)
	END_VAR
END_FUNCTION''')

    type = lib / f'{name}.typ'
    type.write_text('''TYPE 
 
END_TYPE ''')
    
    var = lib / f'{name}.var'
    var.write_text('''VAR CONSTANT 
 
END_VAR ''')

@pytest.fixture
def logical(tmp_path):
    logical = tmp_path / "Logical"
    logical.mkdir()
    package = logical / "Package.pkg"
    package.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<Package Version="1.00.0" xmlns="http://br-automation.co.at/AS/Package">
  <Objects>
    <Object Type="File" Description="Global data types">Global.typ</Object>
    <Object Type="File" Description="Global variables">Global.var</Object>
    <Object Type="Package" Description="Global libraries">Libraries</Object>
  </Objects>
</Package>''')
    global_var = logical / "Global.var"
    global_var.write_text('''
VAR

END_VAR

VAR CONSTANT

END_VAR
''')
    global_typ = logical / "Global.typ"
    global_typ.write_text('''
TYPE

END_TYPE''')
    libraries = logical / "Libraries"
    libraries.mkdir()
    package = libraries / "Package.pkg"
    package.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<Package xmlns="http://br-automation.co.at/AS/Package">
  <Objects>
    <Object Type="Library" Language="binary" Description="This library contains function interfaces for IEC 61131-3 operator functions. For the most part, these are mathematical and logical functions.">operator</Object>
    <Object Type="Library" Language="binary" Description="This library contains runtime functions for IEC tasks.">runtime</Object>
    <Object Type="Library" Language="binary" Description="The SYS_LIB library contains functions for memory management and operating system manipulation as well as hardware-specific functions.">sys_lib</Object>
  </Objects>
</Package>''')
    make_lib(libraries, 'operator')
    make_lib(libraries, 'runtime')
    make_lib(libraries, 'sys_lib')

    yield logical

@pytest.fixture
def binaries(tmp_path):
    binaries = tmp_path / "Binaries"
    if (not path.exists(binaries)):
      binaries.mkdir()
    yield binaries

@pytest.fixture
def objects(temp):
    objects = (temp / "Objects")
    if (not path.exists(objects)):
      objects.mkdir()
    yield objects

@pytest.fixture
def archives(temp):
    archive = (temp / "Archives")
    if (not path.exists(archive)):
      archive.mkdir()
    yield archive

@pytest.fixture
def includes(temp):
    includes = (temp / "Includes")
    if (not path.exists(includes)):
      includes.mkdir()
    yield includes

@pytest.fixture
def temp(tmp_path):
    temp = tmp_path / "Temp"
    if (not path.exists(temp)):
      temp.mkdir()
    yield temp

@pytest.fixture
def source_library_c(logical):
    lib_folder = logical / "Libraries" / "Test_lib"
    lib_folder.mkdir()
    ansi_c = lib_folder / "ANSIC.lby"
    ansi_c.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<Library Version="2.30.1" SubType="ANSIC" xmlns="http://br-automation.co.at/AS/Library">
  <Files>
    <File Description="Exported data types">Test_lib.typ</File>
    <File Description="Exported constants">Test_lib.var</File>
    <File Description="Exported functions and function blocks">Test_lib.fun</File>
    <File>Test_lib.c</File>
  </Files>
  <Dependencies>
    <Dependency ObjectName="astime" />
    <Dependency ObjectName="FileIO" />
    <Dependency ObjectName="Runtime" />
  </Dependencies>
</Library>''')
    typ = lib_folder / "Test_lib.typ"
    typ.write_text('''TYPE
END_TYPE''')
    var = lib_folder / "Test_lib.var"
    var.write_text('''VAR CONSTANT
END_VAR''')
    fun = lib_folder / "Test_lib.fun"
    fun.write_text('''FUNCTION Test_Function : UDINT
	VAR_INPUT
	END_VAR
END_FUNCTION''')
    souce = lib_folder / "Test_lib.c"
    souce.write_text('''
#include <Test_lib.h>
UDINT Test_Function(void)
{
    return 0;
}
''')
    package = ET.parse(logical / "Libraries" / "Package.pkg")
    ET.register_namespace('', 'http://br-automation.co.at/AS/Package')
    lib_element = ET.Element('{http://br-automation.co.at/AS/Package}' + 'Object', Type="Library", Language="ANSIC" )
    lib_element.text = 'Test_lib'
    package.getroot().find('{http://br-automation.co.at/AS/Package}' + 'Objects').append(lib_element)
    package.write(logical / "Libraries" / "Package.pkg", xml_declaration=True, encoding='utf-8')

@pytest.fixture
def config1(tmp_path, physical, temp, binaries, archives, includes, objects):
    config = physical / "Config1"
    config.mkdir()
    package = config / "Config.pkg"
    package.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<Configuration xmlns="http://br-automation.co.at/AS/Configuration">
  <Objects>
    <Object Type="File" Description="Hardware configuration">Hardware.hw</Object>
    <Object Type="File" Description="Hardware topology">Hardware.hwl</Object>
    <Object Type="Cpu">PC</Object>
  </Objects>
  <Sources Download="false" IncludeUpgrades="true" Mode="ProjectTransfer" Option="Complete" />
</Configuration>''')
    
    hardware = config / "Hardware.hw"
    hardware.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio Version=4.12.2.93 FileVersion="4.9"?>
<Hardware xmlns="http://br-automation.co.at/AS/Hardware">
  <Module Name="PC" Type="PC_any" Version="1.1.1.0" OrderNumber="PC">
    <Parameter ID="ConfigurationID" Value="NewEmptySim_Config1" />
    <Parameter ID="Cyclic8Stack" Value="20480" />
    <Parameter ID="UserPartitionSize" Value="256" />
    <Group ID="FileDevice1" />
    <Parameter ID="FileDeviceName1" Value="USER" />
    <Parameter ID="FileDevicePath1" Value="USER_PATH" />
    <Group ID="FileDevice2" />
    <Parameter ID="FileDeviceName2" Value="mappAlarmXFiles" />
    <Parameter ID="FileDevicePath2" Value="USER_PATH:\\AlarmX" />
    <Group ID="FileDevice3" />
    <Parameter ID="FileDeviceName3" Value="mappBackupFiles" />
    <Parameter ID="FileDevicePath3" Value="USER_PATH:\\Backup" />
    <Group ID="FileDevice4" />
    <Parameter ID="FileDeviceName4" Value="mappRecipeFiles" />
    <Parameter ID="FileDevicePath4" Value="USER_PATH:\\Recipe" />
    <Group ID="FileDevice5" />
    <Parameter ID="FileDeviceName5" Value="mappUserXFiles" />
    <Parameter ID="FileDevicePath5" Value="USER_PATH:\\UserX" />
    <Group ID="FileDevice6" />
    <Parameter ID="FileDeviceName6" Value="mappAuditFiles" />
    <Parameter ID="FileDevicePath6" Value="USER_PATH:\\Audit" />
    <Group ID="FileDevice7" />
    <Parameter ID="FileDeviceName7" Value="mappDataFiles" />
    <Parameter ID="FileDevicePath7" Value="USER_PATH:\\Data" />
    <Group ID="FileDevice8" />
    <Parameter ID="FileDeviceName8" Value="mappReportFiles" />
    <Parameter ID="FileDevicePath8" Value="USER_PATH:\\Report" />
    <Group ID="FileDevice9" />
    <Parameter ID="FileDeviceName9" Value="mappPackMLFiles" />
    <Parameter ID="FileDevicePath9" Value="USER_PATH:\\PackML" />
  </Module>
</Hardware>''')
    
    hardware = config / "Hardware.hwl"
    hardware.write_text('''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<?AutomationStudio FileVersion="4.9"?>
<BR.AS.HardwareTopology>
  <TimeStamps>
    <TimeStamp LogicalPath="Config1.Hardware.hw" LastWriteTime="03/30/2022 07:20:13" />
  </TimeStamps>
  <Modules>
    <Module Name="PC" Type="PC_any" X="100" Y="100" />
  </Modules>
  <Links />
  <InfoElements />
</BR.AS.HardwareTopology>''')
    
    pc = config / "PC"
    pc.mkdir()
    cpu = pc / "Cpu.sw"
    cpu.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<SwConfiguration CpuAddress="SL1" xmlns="http://br-automation.co.at/AS/SwConfiguration">
  <TaskClass Name="Cyclic#1" />
  <TaskClass Name="Cyclic#2" />
  <TaskClass Name="Cyclic#3" />
  <TaskClass Name="Cyclic#4" />
  <TaskClass Name="Cyclic#8">
    <Task Name="BackupMgr" Source="Infrastructure.Backup.BackupMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
    <Task Name="FileMgr" Source="Infrastructure.File.FileMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
    <Task Name="UsbMgr" Source="Infrastructure.Usb.UsbMgr.prg" Memory="UserROM" Description="USB manager" Language="IEC" Debugging="true" />
    <Task Name="RecipeMgr" Source="Infrastructure.Recipe.RecipeMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
    <Task Name="UserXMgr" Source="Infrastructure.UserX.UserXMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
    <Task Name="AuditMgr" Source="Infrastructure.Audit.AuditMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
    <Task Name="ReportMgr" Source="Infrastructure.Report.ReportMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
    <Task Name="PackMLMgr" Source="Infrastructure.PackML.PackMLMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
  </TaskClass>
  <Libraries>
    <LibraryObject Name="operator" Source="Libraries.operator.lby" Memory="UserROM" Language="binary" Debugging="true" />
    <LibraryObject Name="sys_lib" Source="Libraries.sys_lib.lby" Memory="UserROM" Language="binary" Debugging="true" />
    <LibraryObject Name="runtime" Source="Libraries.runtime.lby" Memory="UserROM" Language="binary" Debugging="true" />
  </Libraries>
</SwConfiguration>''')
    
    package = pc / "Cpu.pkg"
    package.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<Cpu xmlns="http://br-automation.co.at/AS/Cpu">
  <Objects>
    <Object Type="File" Description="Software configuration">Cpu.sw</Object>
    <Object Type="File" Description="Permanent variables">Cpu.per</Object>
  </Objects>
  <Configuration ModuleId="PC_any">
    <AutomationRuntime Version="B4.92" />
    <Build GccVersion="4.1.2" />
    <DefaultTargetMemory Tasks="UserROM" />
    <Safety SafetyRelease="0.0" />
    <Simulation StartAR000="False" />
    <Vc FirmwareVersion="V4.72.5" />
  </Configuration>
</Cpu>''')
    
    cpu = pc / "Cpu.per"
    cpu.write_text('''VAR_CONFIG
END_VAR''')
    package = ET.parse(physical / "Physical.pkg")
    ET.register_namespace('', 'http://br-automation.co.at/AS/Physical')
    configuration_element = ET.Element('{http://br-automation.co.at/AS/Physical}' + 'Object', Type="Configuration")
    configuration_element.text = 'Config1'
    package.getroot().find('{http://br-automation.co.at/AS/Physical}' + 'Objects').append(configuration_element)
    package.write(physical / "Physical.pkg", xml_declaration=True, encoding='utf-8')

    Export.projectPath = physical
    Export.physicalDir = 'Config1'

    (objects / "Config1").mkdir()
    (objects / "Config1" / "ConfigurationOptions.opt").write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio Version="4.10.5.38 SP"?>
<ConfigurationOptions
  Name="Simulation"
  Target="SG4"
  GccVersion="6.3.0"
  SaveSourceOnTarget="false"
  ActivateSdm="true"
  WebServer="true"
  ARMSimulation="False"
  ArVersion="E4.91">
  <ModuleMemoryData>
    <Module
      Name=""
      Memory="4096" />
  </ModuleMemoryData>
  <Memories
    PermanentAnalogMemory="0"
    PermanentDigitalMemory="0"
    VolatileMemory="65535" />
</ConfigurationOptions>''')

    include_file = includes / "Test_lib.h"
    include_file.write_text('''/* Automation Studio generated header file */
/* Do not edit ! */
/* Test_Lib 1.00.1 */

#ifndef _TEST_LIB_
#define _TEST_LIB_
#ifdef __cplusplus
extern "C" 
{
#endif
#ifndef _Test_Lib_VERSION
#define _Test_Lib_VERSION 1.00.1
#endif

#include <bur/plctypes.h>

#ifndef _BUR_PUBLIC
#define _BUR_PUBLIC
#endif
#ifdef _SG3
		#include "runtime.h"
		#include "astime.h"
		#include "FileIO.h"
#endif

#ifdef _SG4
		#include "runtime.h"
		#include "astime.h"
		#include "FileIO.h"
#endif

#ifdef _SGC
		#include "runtime.h"
		#include "astime.h"
		#include "FileIO.h"
#endif

/* Constants */

/* Datatypes and datatypes of function blocks */

/* Prototyping of functions and function blocks */
_BUR_PUBLIC unsigned long Test_Function(void);

#ifdef __cplusplus
};
#endif
#endif /* _TEST_LIB_ */
''')
    
    (archives / "Config1").mkdir()
    (archives / "Config1" / "PC").mkdir()
    archive_file = archives / "Config1" / "PC" / "libTest_lib.a"
    archive_file.write_text('''just some text, not an actual archive''')
    
    (binaries / "Config1").mkdir()
    (binaries / "Config1" / "PC").mkdir()
    
    br_file = binaries / "Config1" / "PC" / "Test_lib.br"
    br_file.write_text('''just some text, not an actual br file''')
    
    yield config

@pytest.fixture
def config_x20(tmp_path, physical, binaries):
    config = physical / "Config_X20"
    config.mkdir()
    package = config / "Config.pkg"
    package.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<Configuration xmlns="http://br-automation.co.at/AS/Configuration">
  <Objects>
    <Object Type="File" Description="Hardware configuration">Hardware.hw</Object>
    <Object Type="File" Description="Hardware topology">Hardware.hwl</Object>
    <Object Type="Cpu">X20CP1685</Object>
  </Objects>
  <Sources Download="false" IncludeUpgrades="true" Mode="ProjectTransfer" Option="Complete" />
</Configuration>''')
    
    hardware = config / "Hardware.hw"
    hardware.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio Version=4.11.4.55 FileVersion="4.9"?>
<Hardware xmlns="http://br-automation.co.at/AS/Hardware">
  <Module Name="8YFLM01.0000.00I-1" Type="8YFLM01.0000.00I-1" Version="0.0.0.1">
    <Connection Connector="PLK1" TargetModule="X20CP1685" TargetConnector="IF3" NodeNumber="1">
      <Cable Type="PowerlinkCable" Length="10" Version="1.0.0.3" />
    </Connection>
    <Parameter ID="Supervision" Value="off" />
  </Module>
  <Module Name="X20CP1685" Type="X20CP1685" Version="1.7.2.0">
    <Connector Name="IF2">
      <Parameter ID="ActivateDevice" Value="1" />
      <Parameter ID="HostName" Value="innospace6dsim_plc_1" />
      <Parameter ID="Mode" Value="Manual" />
      <Parameter ID="InternetAddress" Value="10.1.13.93" />
      <Parameter ID="SubnetMask" Value="255.255.255.0" />
      <Parameter ID="ActivateSnmp" Value="2" />
    </Connector>
    <Connector Name="IF3">
      <Parameter ID="EplHostName" Value="innospace6dsim_plc_1" />
      <Parameter ID="CycleTime" Value="1000" />
      <Parameter ID="HostName" Value="innospace6dsim_plc_1" />
    </Connector>
    <Parameter ID="ConfigurationID" Value="InnoSpaceSim_X20" />
    <Parameter ID="UserRamSize" Value="15000" />
    <Parameter ID="RemMemSize" Value="15000" />
    <Parameter ID="RemanentGlobalPvSize" Value="1000" />
    <Parameter ID="TimerDeviceType" Value="EPLX2X" />
    <Parameter ID="TimerDevice" Value="X20CP1685.IF3" />
    <Parameter ID="TaskClassIdleTime" Value="2000" />
    <Parameter ID="Cyclic1Duration" Value="2000" />
    <Parameter ID="Cyclic1Tolerance" Value="0" />
    <Parameter ID="Cyclic2Duration" Value="4000" />
    <Parameter ID="Cyclic2Tolerance" Value="4000" />
    <Parameter ID="Cyclic3Duration" Value="8000" />
    <Parameter ID="Cyclic3Tolerance" Value="8000" />
    <Parameter ID="Cyclic4Duration" Value="16000" />
    <Parameter ID="Cyclic4Tolerance" Value="16000" />
    <Parameter ID="Cyclic5Duration" Value="32000" />
    <Parameter ID="Cyclic5Tolerance" Value="32000" />
    <Parameter ID="Cyclic6Duration" Value="64000" />
    <Parameter ID="Cyclic6Tolerance" Value="64000" />
    <Parameter ID="Cyclic7Duration" Value="128000" />
    <Parameter ID="Cyclic7Tolerance" Value="128000" />
    <Parameter ID="Cyclic8Duration" Value="2000" />
    <Group ID="FileDevice1" />
    <Parameter ID="FileDeviceName1" Value="6DMacro" />
    <Parameter ID="FileDevicePath1" Value="F:\Macros" />
    <Group ID="FileDevice2" />
    <Parameter ID="FileDeviceName2" Value="CNC_PrgDir" />
    <Parameter ID="FileDevicePath2" Value="F:/Programs/" />
    <Group ID="FileDevice3" />
    <Parameter ID="FileDeviceName3" Value="Recipe" />
    <Parameter ID="FileDevicePath3" Value="F:/Recipes/" />
    <Group ID="FileDevice4" />
    <Parameter ID="FileDeviceName4" Value="TeachFileDev" />
    <Parameter ID="FileDevicePath4" Value="F:/Teach/" />
    <Group ID="FileDevice5" />
    <Parameter ID="FileDeviceName5" Value="SvMovies" />
    <Parameter ID="FileDevicePath5" Value="F:/SvMovie" />
    <Group ID="FileDevice6" />
    <Parameter ID="FileDeviceName6" Value="User" />
    <Parameter ID="FileDevicePath6" Value="F:\" />
    <Group ID="FileDevice7" />
    <Parameter ID="FileDeviceName7" Value="6DData" />
    <Parameter ID="FileDevicePath7" Value="C:\" />
    <Parameter ID="EthernetHostName" Value="innospace6dsim_plc_1" />
    <Parameter ID="EthernetDefaultGateway" Value="10.1.13.1" />
    <Parameter ID="ActivateDns" Value="1" />
    <Parameter ID="DnsServer1" Value="10.1.10.30" />
    <Parameter ID="DnsServer2" Value="10.43.10.25" />
    <Group ID="FtpUser1" />
    <Parameter ID="FtpUsername1" Value="bur" Description="user" />
    <Parameter ID="FtpUserPassword1" Value="kzPdX7T05qFX/2O0oq22KZRISpE2rDw4PeEeBt2Wff8=" Description="user" />
    <Parameter ID="FtpUserSalt1" Value="NaiTqhR1" />
    <Parameter ID="FTPAccessRight1" Value="0" />
    <Parameter ID="FTPdevice1" Value="ALL" />
    <Parameter ID="WebServerWebDir" Value="site\" />
    <Parameter ID="ActivateOpcUa" Value="1" />
    <Parameter ID="OpcUaInformationModels_PV_Version" Value="1" />
  </Module>
</Hardware>''')
    
    hardware = config / "Hardware.hwl"
    hardware.write_text('''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<?AutomationStudio FileVersion="4.9"?>
<BR.AS.HardwareTopology>
  <TimeStamps>
    <TimeStamp LogicalPath="X20CP1685.Hardware.hw" LastWriteTime="07/22/2022 13:12:45" />
  </TimeStamps>
  <Modules>
    <Module Name="8YFLM01.0000.00I-1" Type="8YFLM01.0000.00I-1" X="338" Y="363" />
    <Module Name="X20CP1685" Type="X20CP1685" X="70" Y="70" />
  </Modules>
  <Links>
    <Link From="8YFLM01.0000.00I-1" To="X20CP1685" FromPort="PLK1" ToPort="IF3" IsRoutedByUser="False">
      <Point X="126" Y="157" />
      <Point X="126" Y="157" />
      <Point X="126" Y="170" />
      <Point X="126" Y="425" />
      <Point X="371" Y="425" />
      <Point X="371" Y="414" />
      <Point X="371" Y="407" />
      <Point X="371" Y="407" />
    </Link>
  </Links>
  <InfoElements />
</BR.AS.HardwareTopology>''')
    
    pc = config / "X20CP1685"
    pc.mkdir()
    cpu = pc / "Cpu.sw"
    cpu.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<SwConfiguration CpuAddress="SL1" xmlns="http://br-automation.co.at/AS/SwConfiguration">
  <TaskClass Name="Cyclic#1" />
  <TaskClass Name="Cyclic#2" />
  <TaskClass Name="Cyclic#3" />
  <TaskClass Name="Cyclic#4" />
  <TaskClass Name="Cyclic#8">
    <Task Name="BackupMgr" Source="Infrastructure.Backup.BackupMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
    <Task Name="FileMgr" Source="Infrastructure.File.FileMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
    <Task Name="UsbMgr" Source="Infrastructure.Usb.UsbMgr.prg" Memory="UserROM" Description="USB manager" Language="IEC" Debugging="true" />
    <Task Name="RecipeMgr" Source="Infrastructure.Recipe.RecipeMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
    <Task Name="UserXMgr" Source="Infrastructure.UserX.UserXMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
    <Task Name="AuditMgr" Source="Infrastructure.Audit.AuditMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
    <Task Name="ReportMgr" Source="Infrastructure.Report.ReportMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
    <Task Name="PackMLMgr" Source="Infrastructure.PackML.PackMLMgr.prg" Memory="UserROM" Language="IEC" Debugging="true" />
  </TaskClass>
  <Libraries>
    <LibraryObject Name="operator" Source="Libraries.operator.lby" Memory="UserROM" Language="binary" Debugging="true" />
    <LibraryObject Name="sys_lib" Source="Libraries.sys_lib.lby" Memory="UserROM" Language="binary" Debugging="true" />
    <LibraryObject Name="runtime" Source="Libraries.runtime.lby" Memory="UserROM" Language="binary" Debugging="true" />
  </Libraries>
</SwConfiguration>''')
    
    package = pc / "Cpu.pkg"
    package.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<Cpu xmlns="http://br-automation.co.at/AS/Cpu">
  <Objects>
    <Object Type="File" Description="Software configuration">Cpu.sw</Object>
    <Object Type="File" Description="Permanent variables">Cpu.per</Object>
  </Objects>
  <Configuration ModuleId="X20CP1685">
    <AutomationRuntime Version="B4.92" />
    <Build GccVersion="6.3.0" />
    <DefaultTargetMemory Tasks="UserROM" />
    <Safety SafetyRelease="0.0" />
  </Configuration>
</Cpu>''')
    
    cpu = pc / "Cpu.per"
    cpu.write_text('''VAR_CONFIG

END_VAR''')
    package = ET.parse(physical / "Physical.pkg")
    ET.register_namespace('', 'http://br-automation.co.at/AS/Physical')
    configuration_element = ET.Element('{http://br-automation.co.at/AS/Physical}' + 'Object', Type="Configuration")
    configuration_element.text = 'Config_X20'
    package.getroot().find('{http://br-automation.co.at/AS/Physical}' + 'Objects').append(configuration_element)
    package.write(physical / "Physical.pkg", xml_declaration=True, encoding='utf-8')

    Export.projectPath = physical
    Export.physicalDir = 'Config_X20'

    (binaries / "Config_X20").mkdir()
    (binaries / "Config_X20" / "X20CP1685").mkdir()

    yield config

@pytest.fixture
def config_arm(tmp_path, physical, temp, binaries, archives, includes, objects):
    config = physical / "Config_Arm"
    config.mkdir()
    package = config / "Config.pkg"
    package.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio Version=4.3.4.121 SP?>
<Configuration xmlns="http://br-automation.co.at/AS/Configuration">
  <Objects>
    <Object Type="File" Description="Hardware configuration">Hardware.hw</Object>
    <Object Type="File" Description="Hardware topology">Hardware.hwl</Object>
    <Object Type="Cpu">4PPC30_043F_21B</Object>
  </Objects>
  <Sources Download="false" IncludeUpgrades="true" Mode="ProjectTransfer" Option="Complete" />
</Configuration>''')
    
    hardware = config / "Hardware.hw"
    hardware.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio Version=4.3.8.58 SP?>
<Hardware xmlns="http://br-automation.co.at/AS/Hardware">
  <Module Name="4PPC30_043F_21B" Type="4PPC30.043F-21B" Version="1.0.1.0">
    <Connector Name="IF3">
      <Parameter ID="ActivateDevice" Value="1" />
    </Connector>
    <Parameter ID="ConfigurationID" Value="string_utils_SG4_Arm" />
    <Parameter ID="TimerDeviceType" Value="SWIOTIMER" />
    <Parameter ID="Cyclic1Duration" Value="10000" />
    <Parameter ID="Cyclic1Tolerance" Value="10000" />
    <Parameter ID="Cyclic2Duration" Value="20000" />
    <Parameter ID="Cyclic2Tolerance" Value="20000" />
    <Parameter ID="Cyclic3Duration" Value="50000" />
    <Parameter ID="Cyclic3Tolerance" Value="50000" />
    <Parameter ID="Cyclic4Duration" Value="100000" />
    <Parameter ID="Cyclic4Tolerance" Value="100000" />
    <Parameter ID="Cyclic5Duration" Value="200000" />
    <Parameter ID="Cyclic5Tolerance" Value="200000" />
    <Parameter ID="Cyclic6Duration" Value="500000" />
    <Parameter ID="Cyclic6Tolerance" Value="500000" />
    <Parameter ID="Cyclic7Duration" Value="1000000" />
    <Parameter ID="Cyclic7Tolerance" Value="1000000" />
    <Parameter ID="Cyclic8Duration" Value="10000" />
    <Parameter ID="Cyclic8Tolerance" Value="30000000" />
  </Module>
</Hardware>''')
    hardware = config / "Hardware.hwl"
    hardware.write_text('''''')
    
    pc = config / "4PPC30_043F_21B"
    pc.mkdir()
    cpu = pc / "Cpu.sw"
    cpu.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<SwConfiguration CpuAddress="SL1" xmlns="http://br-automation.co.at/AS/SwConfiguration">
  <TaskClass Name="Cyclic#1" />
  <TaskClass Name="Cyclic#2" />
  <TaskClass Name="Cyclic#3" />
  <TaskClass Name="Cyclic#4">
    <Task Name="test" Source="test.prg" Memory="UserROM" Language="ANSIC" Debugging="true" />
  </TaskClass>
  <TaskClass Name="Cyclic#5" />
  <TaskClass Name="Cyclic#6" />
  <TaskClass Name="Cyclic#7" />
  <TaskClass Name="Cyclic#8" />
  <Binaries>
    <BinaryObject Name="udbdef" Source="" Memory="UserROM" Language="Binary" />
    <BinaryObject Name="TCData" Source="" Memory="SystemROM" Language="Binary" />
    <BinaryObject Name="ashwac" Source="" Memory="UserROM" Language="Binary" />
    <BinaryObject Name="arconfig" Source="" Memory="SystemROM" Language="Binary" />
    <BinaryObject Name="asfw" Source="" Memory="SystemROM" Language="Binary" />
    <BinaryObject Name="ashwd" Source="" Memory="SystemROM" Language="Binary" />
    <BinaryObject Name="iomap" Source="" Memory="UserROM" Language="Binary" />
    <BinaryObject Name="User" Source="" Memory="UserROM" Language="Binary" />
    <BinaryObject Name="Role" Source="" Memory="UserROM" Language="Binary" />
    <BinaryObject Name="sysconf" Source="" Memory="SystemROM" Language="Binary" />
  </Binaries>
  <Libraries>
    <LibraryObject Name="Convert" Source="Libraries.Convert.lby" Memory="UserROM" Language="Binary" Debugging="true" />
    <LibraryObject Name="Runtime" Source="Libraries.Runtime.lby" Memory="UserROM" Language="Binary" Debugging="true" />
    <LibraryObject Name="Operator" Source="Libraries.Operator.lby" Memory="UserROM" Language="Binary" Debugging="true" />
    <LibraryObject Name="snprintf" Source="Libraries.snprintf.lby" Memory="UserROM" Language="ANSIC" Debugging="true" />
    <LibraryObject Name="sscanf" Source="Libraries.sscanf.lby" Memory="UserROM" Language="ANSIC" Debugging="true" />
  </Libraries>
</SwConfiguration>''')
    
    package = pc / "Cpu.pkg"
    package.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<Cpu xmlns="http://br-automation.co.at/AS/Cpu">
  <Objects>
    <Object Type="File" Description="Software configuration">Cpu.sw</Object>
    <Object Type="File" Description="Permanent variables">Cpu.per</Object>
  </Objects>
  <Configuration ModuleId="4PPC30.043F-21B">
    <AutomationRuntime Version="B4.91" />
    <Build GccVersion="4.1.2" />
    <DefaultTargetMemory Tasks="UserROM" />
    <Vc FirmwareVersion="V4.34.1" />
  </Configuration>
</Cpu>''')
    
    cpu = pc / "Cpu.per"
    cpu.write_text('''VAR_CONFIG
END_VAR''')

    package = ET.parse(physical / "Physical.pkg")
    ET.register_namespace('', 'http://br-automation.co.at/AS/Physical')
    configuration_element = ET.Element('{http://br-automation.co.at/AS/Physical}' + 'Object', Type="Configuration")
    configuration_element.text = 'Config_Arm'
    package.getroot().find('{http://br-automation.co.at/AS/Physical}' + 'Objects').append(configuration_element)
    package.write(physical / "Physical.pkg", xml_declaration=True, encoding='utf-8')

    Export.projectPath = physical
    Export.physicalDir = 'Config_Arm'

    (objects / "Config_Arm").mkdir()
    (objects / "Config_Arm" / "ConfigurationOptions.opt").write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio Version="4.12.2.93"?>
<ConfigurationOptions
  Name="SG4_Arm"
  Target="SG4"
  GccVersion="4.1.2"
  SaveSourceOnTarget="false"
  ActivateSdm="true"
  WebServer="true"
  ARMSimulation="False"
  ArVersion="I4.33">
  <ModuleMemoryData>
    <Module
      Name=""
      Memory="0" />
  </ModuleMemoryData>
  <Memories
    PermanentAnalogMemory="0"
    PermanentDigitalMemory="0"
    VolatileMemory="65535" />
</ConfigurationOptions>''')
   
    (objects / "Config_Arm" / "4PPC30_043F_21B").mkdir()
    (objects / "Config_Arm" / "4PPC30_043F_21B" / "ashwd.br.tmp.xml").write_text('''<?xml version="1.0"?>
<?hwc2hwd version="1.1"?>
<HWD Version="2.0" xmlns="http://br-automation.com/AR/IO/HWD">
  <Hardware Family="4" ID="4PPC30.043F-21B" Modno="59774" UseType="1">
    <Parameter ID="CompatibleCpuCode" Value="4PPC30.043F-21B" />
    <Parameter ID="Transparent" Value="1" Type="UDINT" />
    <Parameter ID="HwcCpuSlot" Value="0" Type="UDINT" />
    <Parameter ID="HwcCpuStation" Value="0" Type="UDINT" />
    <Parameter ID="HwcShortName" Value="PPC3x" />
    <Parameter ID="ArModno" Value="59775" Type="UDINT" />
  </Hardware>
</HWD>''')

    include_file = includes / "Test_lib.h"
    include_file.write_text('''/* Automation Studio generated header file */
/* Do not edit ! */
/* Test_Lib 1.00.1 */

#ifndef _TEST_LIB_
#define _TEST_LIB_
#ifdef __cplusplus
extern "C" 
{
#endif
#ifndef _Test_Lib_VERSION
#define _Test_Lib_VERSION 1.00.1
#endif

#include <bur/plctypes.h>

#ifndef _BUR_PUBLIC
#define _BUR_PUBLIC
#endif
#ifdef _SG3
		#include "runtime.h"
		#include "astime.h"
		#include "FileIO.h"
#endif

#ifdef _SG4
		#include "runtime.h"
		#include "astime.h"
		#include "FileIO.h"
#endif

#ifdef _SGC
		#include "runtime.h"
		#include "astime.h"
		#include "FileIO.h"
#endif

/* Constants */

/* Datatypes and datatypes of function blocks */

/* Prototyping of functions and function blocks */
_BUR_PUBLIC unsigned long Test_Function(void);

#ifdef __cplusplus
};
#endif
#endif /* _TEST_LIB_ */
''')

    (archives / "Config_Arm").mkdir()
    (archives / "Config_Arm" / "4PPC30_043F_21B").mkdir()
    archive_file = archives / "Config_Arm" / "4PPC30_043F_21B" / "libTest_lib.a"
    archive_file.write_text('''just some text, not an actual archive''')

    (binaries / "Config_Arm").mkdir()
    (binaries / "Config_Arm" / "4PPC30_043F_21B").mkdir()
    
    br_file = binaries / "Config_Arm" / "4PPC30_043F_21B" / "Test_lib.br"
    br_file.write_text('''just some text, not an actual br file''')

    yield config

@pytest.fixture
def mappViewConfig(config1):
    pc = config1 / "PC"
    mappView = config1 / "PC" / "mappView"
    mappView.mkdir()
    package = mappView / "Config.pkg"
    package.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<Configuration>
  <Element ID="MappViewConfiguration" Type="MAPPVIEWCFG">
    <Group ID="Server">
      <Selector ID="WebServerProtocol" Value="1">
        <Property ID="WebServerPort" Value="81" />
      </Selector>
      <Property ID="MaxClientConnections" Value="10" />
      <Property ID="MaxBRClientConnections" Value="0" />
      <Selector ID="AuthenticationMode" Value="AuthenticationModeMpUserX">
        <Property ID="MpUserXUserPreferences" Value="TRUE" />
      </Selector>
      <Group ID="TcpProxyConf">
        <Selector ID="InsecureMode" Value="1" />
      </Group>
      <Group ID="DiagnosticPageConf">
        <Selector ID="DiagnosticPageSelection" Value="2">
          <Property ID="DiagnosticPageRole[1]" Value="Administrators" />
        </Selector>
      </Group>
      <Selector ID="Deployment" Value="DeploymentPLC" />
    </Group>
    <Group ID="OpcUa">
      <Property ID="ServerConnectionTimeout" Value="5000" />
      <Group ID="SamplingRates">
        <Property ID="default" Value="200" />
        <Property ID="slow" Value="1000" />
        <Property ID="fast" Value="100" />
      </Group>
      <Property ID="InitValueChangedEvents" Value="TRUE" />
    </Group>
    <Group ID="Timer">
      <Group ID="Timer[1]">
        <Property ID="TimerId" Value="Timer1" />
        <Property ID="TimerInterval" Value="100" />
        <Selector ID="TimerModus" Value="TimerModeSingleShot" />
      </Group>
    </Group>
    <Group ID="Client">
      <Group ID="ContentCaching">
        <Property ID="cachingSlots" Value="200" />
        <Property ID="preserveOldValues" Value="TRUE" />
      </Group>
      <Property ID="defaultVisu" Value="mappFrameworkVis" />
      <Group ID="Widget">
        <Selector ID="renderingPolicy" Value="1" />
      </Group>
    </Group>
  </Element>
</Configuration>''')

    config = mappView / "Config.mappviewcfg"
    config.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<Configuration>
  <Element ID="MappViewConfiguration" Type="MAPPVIEWCFG">
    <Group ID="Server">
      <Selector ID="WebServerProtocol" Value="1">
        <Property ID="WebServerPort" Value="81" />
      </Selector>
      <Property ID="MaxClientConnections" Value="10" />
      <Property ID="MaxBRClientConnections" Value="0" />
      <Selector ID="AuthenticationMode" Value="AuthenticationModeMpUserX">
        <Property ID="MpUserXUserPreferences" Value="TRUE" />
      </Selector>
      <Group ID="TcpProxyConf">
        <Selector ID="InsecureMode" Value="1" />
      </Group>
      <Group ID="DiagnosticPageConf">
        <Selector ID="DiagnosticPageSelection" Value="2">
          <Property ID="DiagnosticPageRole[1]" Value="Administrators" />
        </Selector>
      </Group>
      <Selector ID="Deployment" Value="DeploymentPLC" />
    </Group>
    <Group ID="OpcUa">
      <Property ID="ServerConnectionTimeout" Value="5000" />
      <Group ID="SamplingRates">
        <Property ID="default" Value="200" />
        <Property ID="slow" Value="1000" />
        <Property ID="fast" Value="100" />
      </Group>
      <Property ID="InitValueChangedEvents" Value="TRUE" />
    </Group>
    <Group ID="Timer">
      <Group ID="Timer[1]">
        <Property ID="TimerId" Value="Timer1" />
        <Property ID="TimerInterval" Value="100" />
        <Selector ID="TimerModus" Value="TimerModeSingleShot" />
      </Group>
    </Group>
    <Group ID="Client">
      <Group ID="ContentCaching">
        <Property ID="cachingSlots" Value="200" />
        <Property ID="preserveOldValues" Value="TRUE" />
      </Group>
      <Property ID="defaultVisu" Value="mappFrameworkVis" />
      <Group ID="Widget">
        <Selector ID="renderingPolicy" Value="1" />
      </Group>
    </Group>
  </Element>
</Configuration>''')

    package = ET.parse(pc / "Cpu.pkg")
    ET.register_namespace('', 'http://br-automation.co.at/AS/Cpu')
    mappView_element = ET.Element('{http://br-automation.co.at/AS/Cpu}' + 'Object', Type="Package")
    mappView_element.text = 'mappView'
    package.getroot().find('{http://br-automation.co.at/AS/Cpu}' + 'Objects').append(mappView_element)
    package.write(pc / "Cpu.pkg", xml_declaration=True, encoding='utf-8')

    yield mappView

@pytest.fixture
def physical(tmp_path):
    physical = tmp_path / "Physical"
    physical.mkdir()
    package = physical / "Physical.pkg"
    package.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio FileVersion="4.9"?>
<Physical xmlns="http://br-automation.co.at/AS/Physical">
  <Objects/>
</Physical>''')
    yield physical
    
@pytest.fixture
def project(tmp_path):
    project = tmp_path
    project_file = project / "test.apj"
    project_file.write_text('''<?xml version="1.0" encoding="utf-8"?>
<?AutomationStudio Version="4.12.2.93" WorkingVersion="4.12"?>
<Project Version="1.00.0" Edition="Standard" EditionComment="Standard" xmlns="http://br-automation.co.at/AS/Project">
  <Communication />
  <ANSIC DefaultIncludes="true" />
  <IEC ExtendedConstants="true" IecExtendedComments="true" KeywordsAsStructureMembers="false" NamingConventions="true" Pointers="true" Preprocessor="false" />
  <Motion RestartAcoposParameter="true" RestartInitParameter="true" />
  <Project StoreRuntimeInProject="false" />
  <Variables DefaultInitValue="0" DefaultRetain="false" DefaultVolatile="true" />
  <TechnologyPackages>
    <mapp Version="5.24.0" />
    <mappView Version="5.24.0" />
  </TechnologyPackages>
</Project>"''')
    yield project

@pytest.fixture
def export(tmp_path):
    export = tmp_path / 'export'
    export.mkdir()
    yield export