import argparse
import shutil
import subprocess, shlex
import winreg
from pathlib import Path
import os
from DirUtils import CreateDirectory, removeDir, CleanDirectory

homeDir = ''

def FixHelpNDocRegistry():
    aKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\IBE Software\HelpNDoc\V6', 0, winreg.KEY_ALL_ACCESS)
    userTemplate = winreg.QueryValueEx(aKey, 'UserPathTemplates')[0]
    print(userTemplate)
    if (userTemplate == ''):
        winreg.SetValueEx(aKey, 'UserPathTemplates', 0, winreg.REG_SZ, rf'{homeDir}\Documents\HelpNDoc\Templates\\')
    winreg.CloseKey(aKey)

def UpdateTemplate(helpTemplate) -> bool:
    documentDir = rf'{homeDir}\Documents'
    CreateDirectory(rf'{documentDir}\HelpNDoc')
    CreateDirectory(rf'{documentDir}\HelpNDoc\Templates')
    CleanDirectory(rf'{documentDir}\HelpNDoc\Templates\\')
    removeDir(rf'{documentDir}\HelpNDoc\Templates\\')
    shutil.copytree(rf'{helpTemplate}',rf'{documentDir}\HelpNDoc\Templates')
    return True

def BuildHelp(projectDir, fileName, outputDir, name, language) -> bool:
    CreateDirectory(rf'{projectDir}\{outputDir}')
    CreateDirectory(rf'{projectDir}\{outputDir}\Help-{language}')
    CreateDirectory(rf'{projectDir}\{outputDir}\Help-{language}\{name}Help')
    CreateDirectory(rf'{projectDir}\{outputDir}\Help-{language}\{name}Help\{name}Help')
    CleanDirectory(rf'{projectDir}\{outputDir}\Help-{language}\{name}Help\{name}Help')
    buildCmd = os.getenv('HelpNDoc')
    buildCmd = 'E:\\Program Files (x86)\\IBE Software\\HelpNDoc 6\\hnd6.exe'
    if (name.endswith('.hnd')):
        name = name.replace('.hnd', '')
    if (fileName.endswith('.hnd')):
        project = rf'{projectDir}\{fileName}' + ''
    else:
        project = rf'{projectDir}\{fileName}.hnd' + ''
    options = rf'-s build -x="Build HTML documentation" -o="Build HTML documentation:{projectDir}\{outputDir}\Help-{language}\{name}Help\{name}Help\{name}.html"'
    result = subprocess.run(shlex.split(f'"{buildCmd}" "{project}" {options}'))
    print(f'"{buildCmd}" "{project}" {options}')
    return (result.returncode == 0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Project Directory', dest='project', required=True)
    parser.add_argument('-f', '--file', help='file name', dest='file', required=False, default='')
    parser.add_argument('-n', '--name', help='name', dest='name', required=True)
    parser.add_argument('-o', '--output', help='relative path to the output directory', dest='output', required=False, default='\\ReleaseBuilder\\InstallerSetup\\Help')
    parser.add_argument('-l', '--language', help='language id', dest='language', required=False, default='en')
    args = parser.parse_args()
    if (args.file == ''):
        args.file = args.name

    homeDir = Path.home()
    # if the build is running as the system (Jenkins) then change the home dir so that the installer is copied to the correct directory
    if homeDir.name.endswith('systemprofile'):
        homeDir = r'C:\Users\buchananw'
    print(homeDir)
    FixHelpNDocRegistry()
    if os.path.isdir(rf'{args.project}\Templates'):
        UpdateTemplate(rf'{args.project}\Templates')
    BuildHelp(args.project, args.file, args.output, args.name, args.language)
