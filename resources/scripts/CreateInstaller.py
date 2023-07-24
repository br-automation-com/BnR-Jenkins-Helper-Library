import argparse
import re
import subprocess, shlex
import sys
import os
from DirUtils import CreateDirectory, CleanDirectory, removeDir

def UpdateVersionNumberInstaller(dir, headerFile, version) -> bool:
    p = re.compile('!define Version ".+"')
    fileName = fr'{dir}\{headerFile}' 
    with open(fileName, 'r') as f:
        filedata = p.sub(f'!define Version "{version}"', f.read())
    with open(fileName, 'w', newline='\r\n') as f:
        f.write(filedata)
    return True

def CreateInstaller(dir, installerFileName, version) -> int:
    installDir = rf'{dir}\Install'
    CreateDirectory(installDir)
    CleanDirectory(installDir)
     
    buildCmd = os.getenv('MakeNsis') 
    project = rf'{dir}\SetupTechnologySolutionComplete.nsi'
    options = f'/V1'
    result = subprocess.run(shlex.split(f'"{buildCmd}" "{project}" "{options}"'))
    return result.returncode

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Project Directory', dest='project', required=True)
    parser.add_argument('-n', '--name', help='Project Name', dest='name', required=True)
    parser.add_argument('-o', '--output', help='Output folder', dest='output', required=False, default='TechnologySolution')
    parser.add_argument('-v', '--version', help='Project Version', dest='version', required=False, default="V0.0.9.000")
    args = parser.parse_args()
    version = args.version.replace('V', '')

    UpdateVersionNumberInstaller(rf'{args.project}', f'Setup{args.name}_TS.nsh', f'{version}')
    returnCode = CreateInstaller(f'{args.project}', f'AS4_TS_{args.name}', f'{version}')
    sys.exit(returnCode)
