import argparse
import json
import os
from os import makedirs, path, listdir
from queue import Empty
import re
from zipfile import ZipFile
import tempfile
import shutil
from pathlib import Path
import glob
import ASProject as ASProject
from DirUtils import removeDir, CreateDirectory, CleanDirectory
import xml.etree.ElementTree as ET

projectPath = ''
physicalDir= ''

def copy(exportDir, f):
    global projectPath
    fullPath = os.path.join(projectPath, f)
    if path.isdir(fullPath):
        shutil.copytree(fullPath, os.path.join(exportDir, f))
    elif path.isfile(fullPath):
        #print(Path(f).parent)
        if (path.exists(os.path.join(exportDir, str(Path(f).parent))) == False):
            os.makedirs(os.path.join(exportDir, str(Path(f).parent)))
        shutil.copy(fullPath, os.path.join(exportDir, f))

def cleanPackageFile(dir, file, compileLibraries):
    files = os.listdir(dir)
    with open(os.path.join(dir, file), "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            object = line[line.find('>') + 1 : line.find('</Objects>') - 9]
            if (object in compileLibraries):
                line = line.replace('ANSIC', 'binary').replace('IEC', 'binary')
            if (object == '') or (object in files):
                f.write(line)
        f.truncate()

def copySwDeployment(dir, tasks, libraries):
    global projectPath
    global physicalDir
    print(projectPath)
    cpuDir = [cpu for cpu in os.listdir(os.path.join(projectPath, physicalDir)) if os.path.isdir(os.path.join(os.path.join(projectPath, physicalDir), cpu))][0]
    file = os.path.join(physicalDir, cpuDir, 'Cpu.sw')
    if (path.exists(os.path.join(dir, physicalDir, cpuDir)) == False):
        os.makedirs(os.path.join(dir, physicalDir, cpuDir))
    shutil.copy(os.path.join(projectPath, file), os.path.join(dir, file))
    with open(os.path.join(dir, file), "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            task = ''
            if (line.find('<Task Name="') != -1):
                 task = line[line.find('Source="') + 8 : line.find('"', line.find('Source="') + 8)]
            lib = ''
            if (line.find('<LibraryObject Name="') != -1):
                 lib = line[line.find('Name="') + 6 : line.find('"', line.find('Name="') + 6)]
            if ((task == '') and (lib == '')) or (task in tasks) or (lib in libraries):
                f.write(line)
        f.truncate()

def copyFileDevices(dir, fileDevices):
    global physicalDir
    file = os.path.join(physicalDir, 'Hardware.hw')
    if (os.path.isfile(os.path.join(dir, file)) == False):
        copy(dir, os.path.join(physicalDir, 'Hardware.hw'))
    fileDeviceIndex = -1
    fileDeviceLines = []
    fileDevice = ''
    with open(os.path.join(dir, file), "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            if (fileDeviceIndex == -1):
                fileDeviceIndex = line.find('<Group ID="FileDevice')
            elif ((line.find('Group ID="') != -1) or (line.find('ID="FileDevice') == -1) and (fileDevice != '')):
                if (fileDevice in fileDevices):
                    for l in fileDeviceLines:
                        f.write(l)
                fileDeviceIndex = line.find('<Group ID="FileDevice')
                fileDeviceLines = []
            if (fileDeviceIndex != -1):
                fileDeviceLines.append(line)
                if ((line.find('FileDeviceName') != -1) and (line.find('Value="') != -1)):
                    fileDevice = line[line.find('Value="') + 7 : line.find('"', line.find('Value="') + 7)]
            if ((fileDeviceIndex == -1) and ((line.find('<?') != -1) or (line.find('Hardware') != -1) or (line.find('<Module ') != -1) or (line.find('</Module') != -1))):
                #print('adding line ' + line)
                f.write(line)
        f.truncate()

def copyVncDevices(dir):
    global projectPath
    global physicalDir
    file = os.path.join(physicalDir, 'Hardware.hw')
    if (os.path.isfile(os.path.join(dir, file)) == False):
        copy(dir, os.path.join(physicalDir, 'Hardware.hw'))
    file = os.path.join(dir, physicalDir, 'Hardware.hw')
    vncIndex = -1
    vncLines = []
    connectorIndex = -1
    connector = ''
    connectorLines = []
    with open(os.path.join(projectPath, physicalDir, 'Hardware.hw'), "r") as f:
        orig_f = f.readlines()
        f.seek(0)
        for line in orig_f:
            if (connectorIndex == -1):
                connectorIndex = line.find('<Connector Name="IF')
                connector = line
            elif (line.find('</Connector>') != -1):
                connectorIndex = -1
                if (len(vncLines) > 0):
                    connectorLines.append(connector)
                    connectorLines += vncLines
                    connectorLines.append('    </Connector>\n')
            if (vncIndex == -1):
                vncIndex = line.find('<Group ID="Vnc')
            elif ((line.find('Group ID="') != -1) or (line.find('ID="Vnc') == -1)):
                vncIndex = line.find('<Group ID="Vnc')
                vncLines = []
            if (vncIndex != -1):
                vncLines.append(line)
    with open(os.path.join(dir, file), "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            f.write(line)
            if (line.find('<Module Name=') != -1):
                for l in connectorLines:
                    f.write(l)
        f.truncate()

def enableOpcUa(dir):
    global physicalDir
    #print('enabling Opcua')
    
    if (os.path.isfile(os.path.join(dir, physicalDir, 'Config.pkg')) == False):
        copy(dir, os.path.join(physicalDir, 'Config.pkg'))
    config = ET.parse(os.path.join(dir, physicalDir, 'Config.pkg'))
    ET.register_namespace('', 'http://br-automation.co.at/AS/Configuration')
    ns = '{http://br-automation.co.at/AS/Configuration}'
    cpu = ''
    for obj in config.getroot().find(ns + 'Objects').findall(ns + 'Object'):
        if (obj.get('Type') == 'Cpu'):
            cpu = obj.text
            break
    
    if (os.path.isfile(os.path.join(dir, physicalDir, cpu, 'Cpu.pkg')) == False):
        copy(dir, os.path.join(physicalDir, cpu, 'Cpu.pkg'))
    package = ET.parse(os.path.join(dir, physicalDir, cpu, 'Cpu.pkg'))
    ns = '{http://br-automation.co.at/AS/Cpu}'
    cpu_module = package.getroot().find(ns + 'Configuration').get('ModuleId')

    if (os.path.isfile(os.path.join(dir, physicalDir, 'Hardware.hw')) == False):
        copy(dir, os.path.join(physicalDir, 'Hardware.hw'))
    ns = '{http://br-automation.co.at/AS/Hardware}'
    ET.register_namespace('', 'http://br-automation.co.at/AS/Hardware')
    hardware = ET.parse(os.path.join(dir, physicalDir, 'Hardware.hw'))
    
    for module in hardware.getroot().findall(ns + 'Module'):
        if module.get('Type') == cpu_module:
            if not module.findall(ns + 'Parameter/[@ID="ActivateOpcUa"]'):
                module.append(ET.Element(ns + 'Parameter', ID='ActivateOpcUa', Value='1'))
            if not module.findall(ns + 'Parameter/[@ID="OpcUaActivateAuditEvents"]'):
                module.append(ET.Element(ns + 'Parameter', ID='OpcUaActivateAuditEvents', Value='1'))        
            if not module.findall(ns + 'Parameter/[@ID="OpcUa_Security_AdminRole"]'):
                module.append(ET.Element(ns + 'Parameter', ID='OpcUa_Security_AdminRole', Value='Administrators'))
            break
    hardware.write(os.path.join(dir, physicalDir, 'Hardware.hw'), xml_declaration=True, encoding='utf-8')

def setUserPartitionSize(dir):
    global projectPath
    global physicalDir
    file = os.path.join(physicalDir, 'Hardware.hw')

    userPartition = ''
    with open(os.path.join(projectPath, file), "r") as f:
        new_f = f.readlines()
        for line in new_f:
            if (line.find('<Parameter ID="UserPartitionSize"') != -1):
                userPartition = line

    with open(os.path.join(dir, file), "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            if (line.find('</Module>') != -1):
                f.write(userPartition)
            f.write(line)
        f.truncate()

def clearAuthentication(dir):
    global physicalDir
    cpuDir = [cpu for cpu in os.listdir(os.path.join(dir, physicalDir)) if os.path.isdir(os.path.join(os.path.join(dir, physicalDir), cpu))][0]
    if (path.exists(os.path.join(dir, physicalDir, cpuDir, 'mappView', 'Config.mappviewcfg')) == False):
        return
    file = os.path.join(dir, physicalDir, cpuDir, 'mappView', 'Config.mappviewcfg')
    with open(file, "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        authModeIndex = -1    
        for line in new_f:
            if (authModeIndex == -1):
                authModeIndex = line.find('<Selector ID="AuthenticationMode"')
            elif (line.find('<Group ID=') != -1):
                authModeIndex = -1
            if (authModeIndex == -1):
                f.write(line)
        f.truncate()

def cleanPackage(exportName, exportDir, compileLibraries):
    global projectPath
    for root, dirs, files in os.walk(exportDir):
        for name in dirs:
            relativePath = os.path.join(root.replace(exportDir, ''), name)
            if (relativePath.startswith('\\')):
                relativePath = relativePath.replace('\\', '', 1)
            exportPackageFile = glob.glob(os.path.join(root, name) + '\\*.pkg')
            projectPackageFile = glob.glob(os.path.join(projectPath, relativePath) + '\\*.pkg')
            if ((len(exportPackageFile) == 0) and (len(projectPackageFile) != 0)):
                shutil.copy(os.path.join(projectPath, relativePath, Path(projectPackageFile[0]).name), os.path.join(exportDir, relativePath, Path(projectPackageFile[0]).name))
                cleanPackageFile(os.path.join(exportDir, relativePath), Path(projectPackageFile[0]).name, compileLibraries)

def standardExport(export, exportDir, project, tasks, libraries = []):
    if ('libraries' in export):
        libraries += export['libraries']
        for l in export['libraries']:
            copy(exportDir, os.path.join('Logical', 'Libraries', l))
    if ('mapp' in export):
        libraries += export['mapp']
        for m in export['mapp']:
            copy(exportDir, os.path.join('Logical', 'Libraries', m))
    if ('compileLibraries' in export):
        libraries += export['compileLibraries']
        for l in export['compileLibraries']:
            lib = project.findLibrary(l)
            if (lib is not None):
                project.exportLibrary(l, exportDir)
                libDir = lib._directory
                libDir = libDir[libDir.index('Logical'):]
                removeDir(os.path.join(exportDir, libDir))
                versionDir = os.path.join(exportDir, l, os.listdir(os.path.join(exportDir, l))[0])
                shutil.copytree(versionDir, os.path.join(exportDir, libDir))
                removeDir(os.path.join(exportDir, l))
    if ('physical' in export):
        copySwDeployment(exportDir, tasks, libraries)
        copyFileDevices(exportDir, export['physical']["fileDevices"])
        if (('enableOpcUa' in export['physical']) and (export['physical']['enableOpcUa'] == True)):
            enableOpcUa(exportDir)
        if (('UserPartitionSize' in export['physical']) and (export['physical']['UserPartitionSize'] == True)):
            setUserPartitionSize(exportDir)

def fileExport(export, exportDir):
    if ('files' in export):
        for f in export['files']:
            copy(exportDir, f)

def parse_bool(s: str) -> bool:
    try:
        return {'true': True, 'false': False}[s.lower()]
    except KeyError:
        raise argparse.ArgumentTypeError(s)
    
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Project Directory', dest='project', required=True)
    parser.add_argument('-c', '--config', help='Configuration File Name', dest='config', required=True)
    parser.add_argument('-s', '--physical', help='Physical Directory', dest='physical', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', dest='output', required=True)
    parser.add_argument('-z', '--zip', help='zip output directory', dest='zip', required=False, default=True)
    parser.add_argument('-v', '--vc4', help='export VC4 files', dest='vc4', required=False, default=True, type=parse_bool)
    global projectPath
    global physicalDir
    args = parser.parse_args()
    projectPath = args.project
    physicalDir = args.physical

    project = ASProject.ASProject(args.project)
    tempDir = tempfile.TemporaryDirectory()    
    exportDir = os.path.join(tempDir.name, Path(args.config).stem)
    CreateDirectory(exportDir)

    config = args.config
    if (path.exists(config) != True):
        print('config file not found in ' + config)
        return 0
    export = json.load(open(config))
    
    if ('physical' in export):
        standardExport(export, exportDir, project, export['physical']["deployTasks"])
    fileExport(export, exportDir)
    compileLibraries = export['compileLibraries'] if ('compileLibraries' in export) else []

    cleanPackage(os.path.join(args.output, Path(args.config).stem), exportDir, compileLibraries)
    if (args.zip == True):
        shutil.make_archive(os.path.join(args.output, Path(args.config).stem), 'zip', exportDir)
    else:
        shutil.copytree(exportDir, os.path.join(args.output, Path(args.config).stem))

    if ('mappViewfiles' in export) == True:
        CleanDirectory(exportDir)
        libraries = []
        for f in export['mappViewfiles']:
            copy(exportDir, f)    
            if ('Libraries' in f):
                libraries.append(f[f.index('Libraries\\') + 10:])
        copySwDeployment(exportDir, export['physical']["deployTasks"], libraries)
        copyFileDevices(exportDir, export['physical']["fileDevices"])
        enableOpcUa(exportDir)
        if not(('SetAuthenticationMode' in export['physical']) and (export['physical']['SetAuthenticationMode'] == True)):
            clearAuthentication(exportDir)
            
        cleanPackage(os.path.join(args.output, Path(args.config).stem + 'MappView'), exportDir, compileLibraries)
        if (args.zip == True):
            shutil.make_archive(os.path.join(args.output, Path(args.config).stem + 'MappView'), 'zip', exportDir)
        else:
            shutil.copytree(exportDir, os.path.join(args.output, Path(args.config).stem + 'MappView'))

    if ((args.vc4 == True) and (('VC4' in export) == True)):
        physicalDir = args.physical + 'VC4'
        CleanDirectory(exportDir)
        libraries = []
        for f in export['VC4']:
            copy(exportDir, f)    
            if ('Libraries' in f):
                libraries.append(f[f.index('Libraries\\') + 10:])
        standardExport(export, exportDir, project, export['physical']["deployTasksVC4"])
        compileLibraries = export['compileLibraries'] if ('compileLibraries' in export) else []
        copyVncDevices(exportDir)
        if (('enableOpcUaVC4' in export['physical']) and (export['physical']['enableOpcUaVC4'] == True)):
            enableOpcUa(exportDir)

        cleanPackage(os.path.join(args.output, Path(args.config).stem + 'VC4'), exportDir, compileLibraries)
        if (args.zip == True):
            shutil.make_archive(os.path.join(args.output, Path(args.config).stem + 'VC4'), 'zip', exportDir)
        else:
            shutil.copytree(exportDir, os.path.join(args.output, Path(args.config).stem + 'VC4'))

if __name__ == '__main__':
    main()
