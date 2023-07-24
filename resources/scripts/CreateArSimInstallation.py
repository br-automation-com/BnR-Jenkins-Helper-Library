
import InstalledAS
import ASProject
import subprocess
import shutil
import sys
import argparse
import tempfile
import re

def CreateSimulationTarget(Project, Configuration, ArSimDir) -> bool:
    print('Creating ArSim installation')
    __projectPath = Project._projectDir
    __compileAsPath = InstalledAS.ASInstallPath(Project)
    if (__compileAsPath == ''):
        return False

    buildCommand = (__compileAsPath + r'\Bin-en\BR.AS.Build.exe '
                        + '"' + __projectPath + '\\' + Project.projectName + '"'
                        + ' -buildMode "Build"'
                        + ' -c ' + Project._configurations[Configuration]._name
                        + ' -buildRUCPackage'
                        + ' -t C:\\Temp\\' + Project._configurations[Configuration]._name
                        )
    result = subprocess.run(buildCommand, cwd=__projectPath, capture_output=True, text=True)
    print(result.stdout)

    tempDir = tempfile.TemporaryDirectory()
    __cpuName = Project._configurations[Configuration]._cpuName

    with open(f'{tempDir.name}\\createArSim.pil', 'x') as f:
        f.write(f'CreateARsimStructure "{__projectPath}\\Binaries\\{Configuration}\\{__cpuName}\\RUCPackage\\RUCPackage.zip", "{ArSimDir}", "Start=-"')

    pviCmd = InstalledAS.PVIPath() + r'\PVI\Tools\PVITransfer\PVITransfer.exe'
    pviOptions = rf'-silent "{tempDir.name}\createArSim.pil"'
    subprocess.run(f'{pviCmd} {pviOptions}')
    print('ArSim created')
    return True

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Project Directory', dest='projectDir', required=True)
    parser.add_argument('-c', '--configuration', help='Configuration to build', dest='config', required=True)
    parser.add_argument('-s', '--simulationDirectory', help='ArSim installation directory', dest='simulationDir', required=True)
    args = parser.parse_args()

    project = ASProject.ASProject(args.projectDir)
    result = CreateSimulationTarget(project, args.config, args.simulationDir)
    sys.exit(0)
    return

if __name__ == '__main__':
    main()