"""
Description: This scipt accepts project location and compile the project with appropriate version of Automation studio project

Usage: AsProjectCompile.py "ProjectPath" "TempPath" "Outputpath"

Returns : Build result
    0 = No Errors
    1 = Warnings
    3 = Build Error

Example: c:/projects/CICD/ASHelperScripts/AsProjectCompile.py "C:/projects/CICD/MachineWVD" "C:/projects/CICD/MachineWVD/Temp" "C:/projects/CICD/MachineWVD/output"

"""

import InstalledAS
import ASProject
import os
import shutil
import sys
import argparse
import tempfile
import re
import subprocess

def PrintErrorsAndWarnings(output):
    regex = re.compile(r'.*(?P<result>error|warning) \d*:.*')
    for l in output:
        matches = re.search(regex, l)
        if (matches != None):
            if (matches.group('result')) == 'error':
                print(f'\033[91m {l} \033[0m')
            elif (matches.group('result')) == 'warning':
                print(f'\033[92m {l} \033[0m')

def Compile(Project, Configuration, BuildPIP, NoClean):
    __projectPath = Project._projectDir
    __compileAsPath = InstalledAS.ASInstallPath(Project)
    __PVIpath = InstalledAS.PVIPath()
    if (__compileAsPath == ''):
        print('no compatible AS installed')
        return [['', '', 3]]

    buildResult = []
    regex = re.compile(r'Build: (\d+) error\(s\), (\d+) warning\(s\)')

    for config in Project._configurations:        
        if (Configuration == Project._configurations[config]._name) or (Configuration == 'all'):
            standard_commands = f'{os.path.join(__compileAsPath, "Bin-en", "BR.AS.Build.exe")} "{os.path.join(__projectPath, Project.projectName)}" -c {Project._configurations[config]._name} -t "{Project._configurations[config].TempDirectory()}" -o "{Project._configurations[config].BinariesDirectory()}"'
            if (NoClean == False):
                result = subprocess.run(standard_commands + ' -cleanAll', cwd=__projectPath, capture_output=True, text=True)
            
            result = subprocess.run(standard_commands + ' -buildMode "Build" -buildRUCPackage', capture_output=True, text=True)
            errors = 0
            warnings = 0
            output = result.stdout.splitlines()
            r = regex.match(output[-2])
            if (r != None):
                errors = int(r.group(1))
                warnings = int(r.group(2))
                if (errors > 0) or (warnings > 0):
                    PrintErrorsAndWarnings(output)
            buildResult.append([Project._configurations[config]._name, result.returncode, errors, warnings])
            print(f'Build Result {Project._configurations[config]._name} = {result.returncode}')

            if (BuildPIP):
                #create PIP
                pilPath = os.path.join(__projectPath, "CreatePIP.pil")
                pilContents = 'CreatePIP "' + os.path.join(__projectPath, Project._configurations[config].BinariesDirectory(), Project._configurations[config]._name, Project._configurations[config]._cpuName, 'RUCPackage', 'RUCPackage.zip') + '", "InstallMode=Consistent InstallRestriction=AllowUpdatesWithoutDataLoss KeepPVValues=1 ExecuteInitExit=0 IgnoreVersion=1 AllowDowngrade=0", "Default", "SupportLegacyAR=1", "DestinationDirectory=\'' + __projectPath + 'PIP\'"'
                pilFile = open(pilPath,"w")
                pilFile.write(pilContents)
                pilFile.close()
                pviTransferPath = os.path.join(__PVIpath, 'PVI', 'Tools', 'PVITransfer', 'PVITransfer.exe')
                pipCommand = (pviTransferPath + ' -silent "' + pilPath + '"')
                result = subprocess.run(pipCommand, cwd=__projectPath, capture_output=True, text=True)
                PrintErrorsAndWarnings(result.stdout.splitlines())
                shutil.make_archive("PIP", 'zip', os.path.join(__projectPath, "PIP"))
                
    return buildResult

def parse_bool(s: str) -> bool:
    try:
        return {'true': True, 'false': False}[s.lower()]
    except KeyError:
        raise argparse.ArgumentTypeError(s)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Project Directory', dest='projectDir', required=True)
    parser.add_argument('-c', '--configuration', help='Configuration to build', dest='config', required=False, default='all')
    parser.add_argument('-w', '--maxwarnings', help='Maximum allowed warnings during build, -1 disables', dest='maxWarnings', required=False, default=-1)
    parser.add_argument('-b', '--buildpip', help='Builds the Project Installation Package', dest='BuildPIP', required=False, default=False, type=parse_bool)
    parser.add_argument('-n', '--no-clean', help='Do not clean the project before building', dest='NoClean', action='store_true')
    args = parser.parse_args()

    project = ASProject.ASProject(args.projectDir)
    results = Compile(project, args.config, args.BuildPIP, args.NoClean)
    compileResult = 0
    maxWarnings = 0
    for result in results:
        compileResult = int(result[1]) if (compileResult < int(result[1])) else compileResult
        maxWarnings = result[3] if ((result[3] > maxWarnings) and (args.maxWarnings != -1)) else maxWarnings

    if (compileResult == 1):
        compileResult = 1 if ((int(args.maxWarnings) > 0) and (maxWarnings > int(args.maxWarnings))) else 0

    print('Build Result = ' + str(compileResult))
    sys.exit(compileResult)

if __name__ == '__main__':
    main()
