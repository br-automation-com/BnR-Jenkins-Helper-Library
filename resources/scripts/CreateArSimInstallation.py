
import InstalledAS
import ASProject
import subprocess
import shutil
import sys
import argparse
import tempfile
import re
import os
from AsProjectCompile import Compile

def CreateSimulationTarget(Project, Configuration, ArSimDir, Clean) -> bool:
    print('Creating ArSim installation')

    Compile(Project, Configuration, False, not Clean)

    tempDir = tempfile.TemporaryDirectory()
    __cpuName = Project._configurations[Configuration]._cpuName

    print(f'{Project._configurations[Configuration].BinariesDirectory()}')

    with open(f'{tempDir.name}\\createArSim.pil', 'x') as f:
        f.write(f'CreateARsimStructure "{Project._configurations[Configuration].BinariesDirectory()}\\{Configuration}\\{__cpuName}\\RUCPackage\\RUCPackage.zip", "{ArSimDir}", "Start=0"')

    pviCmd = InstalledAS.PVIPath() + r'\PVI\Tools\PVITransfer\PVITransfer.exe'
    pviOptions = rf'-silent "{tempDir.name}\createArSim.pil" -consoleOutput'
    result = subprocess.run(f'{pviCmd} {pviOptions}', capture_output=True)
    print(result)
    print('ArSim created')
    return True

def parse_bool(s: str) -> bool:
    try:
        return {'true': True, 'false': False}[s.lower()]
    except KeyError:
        raise argparse.ArgumentTypeError(s)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Project Directory', dest='projectDir', required=True)
    parser.add_argument('-c', '--configuration', help='Configuration to build', dest='config', required=True)
    parser.add_argument('-s', '--simulationDirectory', help='ArSim installation directory', dest='simulationDir', required=True)
    parser.add_argument('-l', '--clean', help='Clean configuration', dest='clean', required=False, default=False, type=parse_bool)
    args = parser.parse_args()

    project = ASProject.ASProject(args.projectDir)
    print(f'{project._configurations[args.config].BinariesDirectory()}')
    result = CreateSimulationTarget(project, args.config, args.simulationDir, args.clean)
    sys.exit(0)

if __name__ == '__main__':
    main()