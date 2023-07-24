# -*- coding: utf-8 -*-
"""
Created on Dec 8, 2022

@author: buchananw
"""

import sys
import argparse
import shutil
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', help='Folder you want to zip', dest='folder', required=True)
    args = parser.parse_args()

    shutil.make_archive(Path(args.folder).stem, 'zip', args.folder)

if __name__ == '__main__':
    main()







