import argparse
import os
import sys
from pathlib import Path

DESCRIPTION = '''
Commonly opened files opened up quick.
Also you can recover files.

If the file normally requires you to run with 'sudo', then you MUST run this in sudo.
The opposite is also true. If user owns the file, then do NOT use sudo.

Usage:
  qk alias                                               Open your file with the default editor.
  qk --recover alias                                     Recover a previously backed up file.
  
  qk --auto-recovery                                     When adding a file to open, also save a backup.
  qk --add-open [Path to file] --alias [Name of file]    Add a file to quickly open under your chosen alias.
  qk --editor [Name of editor]                           Set the default editor.
  qk --add-recovery [Path to file]                       Create a backup file stored by qktool.
'''

IS_SUDO = True if not os.geteuid() == 0 else False
DEFAULTS = [
    '# This is where the config of qktool lives as well as your filepaths.',
    'EDITOR=vi',
    'RECOVERY="~/qktool/recovery.d"'
    'DIR_SUDO="/etc/qktool/recovery.d'
]

def main():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION
    )
    
    parser.add_argument('--add-open', type=str, default='')
    parser.add_argument('--add-recovery')
    
    if IS_SUDO:
        cfgPath = "/etc/qktool/qk.config"
    else:
        cfgPath = "~/qktool/qk.config"
    
    with open(cfgPath, 'a+') as cfgFile:
        cfgFile.seek(0)
        cfg = cfgFile.readlines()
        if not cfg:
            cfgFile.writelines(DEFAULTS)