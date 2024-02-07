
import argparse
import json
import os
import sys
import ASProject
import AsProjectCompile

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Project Directory', dest='projectDir', required=True)
    parser.add_argument('-l', '--library', help='Library to export', dest='library', required=True)
    parser.add_argument('-d', '--directory', help='Directory to export library to', dest='exportLocation', required=False, default='.\\')
    args = parser.parse_args()
    project = ASProject.ASProject(args.projectDir)
    project.exportLibrary(args.library, args.exportLocation)

if __name__ == '__main__':
    main()