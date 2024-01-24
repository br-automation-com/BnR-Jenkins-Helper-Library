import ASProject
import argparse
import glob
from os import path, system, chdir
from subprocess import call
from DirUtils import CleanDirectory

def convertGcovFiles(project: ASProject, config):
    ElfGcov = fr'C:\BrAutomation\AS{project.workingVersion.replace(".","")}\AS\gnuinst\V6.3.0\4.9\bin\i686-elf-gcov.exe'
    pattern = project._configurations[config].TempDirectory() + '/**/*.gcda'
    for file_name in glob.glob(pattern, recursive=True):
        if path.isfile(file_name):
            call([ElfGcov, '-bc', file_name])
    pattern = project._configurations[config].TempDirectory() + '/**/*.gcno'
    for file_name in glob.glob(pattern, recursive=True):
        if path.isfile(file_name):
            call([ElfGcov, '-bc', file_name])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Project Directory', dest='projectDir', required=True)
    parser.add_argument('-c', '--config', help='Configuration', dest='config', required=True)
    parser.add_argument('-o', '--output', help='Output Directory', dest='outputDir', required=False, default='CodeCoverage')
    args = parser.parse_args()

    print("running")
    project = ASProject.ASProject(args.projectDir)
    output = path.join(args.projectDir, args.outputDir)
    CleanDirectory(output)
    chdir(output)
    convertGcovFiles(project, args.config)
    
    system(fr'py -m gcovr -g -k -v --root "{args.projectDir}" --html --html-details -o report.html')
    system(fr'py -m gcovr -g -k -v --root "{args.projectDir}" --xml-pretty -o report.xml')


if __name__ == '__main__':
    main()
