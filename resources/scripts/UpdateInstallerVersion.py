import argparse
import re
from DirUtils import CreateDirectory, CleanDirectory, removeDir

def UpdateVersionNumberInstaller(dir, headerFile, version) -> bool:
    p = re.compile('!define Version ".+"')
    fileName = fr'{dir}\{headerFile}' 
    with open(fileName, 'r') as f:
        filedata = p.sub(f'!define Version "{version}"', f.read())
    with open(fileName, 'w', newline='\r\n') as f:
        f.write(filedata)
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Project Directory', dest='project', required=True)
    parser.add_argument('-n', '--name', help='Project Name', dest='name', required=True)
    parser.add_argument('-v', '--version', help='Project Version', dest='version', required=False, default="V0.0.9.000")
    args = parser.parse_args()
    version = args.version.replace('V', '').replace('v','')

    UpdateVersionNumberInstaller(rf'{args.project}', f'Setup{args.name}_TS.nsh', f'{version}')
