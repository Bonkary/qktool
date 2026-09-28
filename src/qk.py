import argparse
import subprocess
import os
import sys
from pathlib import Path
import shutil


DESCRIPTION = '''
Commonly opened files opened up quick.
Also you can recover files.

If the file normally requires you to run with 'sudo', then you MUST run this in sudo.
The opposite is also true. If user owns the file, then do NOT use sudo.

Usage:
  qk alias                                               Open your file with the default editor.
  qk alias --recover                                     Recover a previously backed up file.
  qk alias --update                                      Update a recovery files.
  
  qk --update-all                                        Update all recovery files
  qk --auto-recovery                                     When adding a file to open, also save a backup.
  qk --add-open [Path to file] --alias [Name of file]    Add a file to quickly open under your chosen alias.
  qk --editor [Name of editor]                           Set the default editor.
  qk --add-recovery [Path to file]                       Create a backup file stored by qktool.
'''
DEFAULT_FILE = [
    '# This is where the config of qktool lives as well as your filepaths.\n',
    'editor=nano\n',
    'autorecovery=no\n',
    '\n[open]\n',
]
DEFAULT_CFG = [
    'editor=nano\n',
    'autorecovery=no\n',
    '\n[open]\n',
]

SUDO = True if os.getuid() == 0 else False
PKG_DIR = Path(__file__).resolve()
USER = os.environ['USER']

def main(args: argparse.Namespace):
    if SUDO:
        cfgPath = "/etc/qktool/qk.config"
    else:
        cfgPath = f"/home/{USER}/qktool/qk.config"
    
    try:
        with open(cfgPath, 'r') as cfgFile:
            cfg = cfgFile.readlines()
            cfg = [line for line in cfg if not "#" in line]
            
    except FileNotFoundError:
        with open(cfgPath, 'w') as cfgFile:
            cfgFile.writelines(DEFAULT_FILE)
            cfg = DEFAULT_CFG
            
    except PermissionError:
        print("Permission denied.")
        sys.exit(1)
        
    for line in cfg:
        if "autorecovery=" in line:
            autoRecovery = line.split("=")[-1].replace("\n", "")

        elif "editor=" in line:
            editor = line.split("=")[-1].replace("\n", "")

        elif f"{args.alias}=" in line:
            aliasPath = line.split("=")[-1].replace("\n", "")

        elif '[open]' in line:
            openIndex = cfg.index(line)
        
    if args.alias:
        if args.recover:
            pass

        elif args.update:
            pass

        else:
            cmd = ['sudo', editor, aliasPath] if SUDO else [editor, aliasPath]
            subprocess.call(cmd)

    elif args.updateAll:
        pass

    elif args.autoRecovery:
        pass

    elif args.addOpen:
        if args.newAlias:
            print(cfg)
            var = args.newAlias + "=" + args.addOpen
            cfg.insert(openIndex+1, var)
            with open(cfgPath, 'w') as cfgFile:
                cfgFile.writelines(cfg)

            if args.recover or autoRecovery:
                filename = args.addOpen.split("/")[-1]
                recovFile = os.path.join("/home", USER, 'qktool', 'recovery.d', filename)
                shutil.copy(src=args.addOpen, dst=recovFile)

        else:
            print("Missing the new alias!")
            sys.exit(1)

    elif args.editor:
        print(cfg)
        cfg[cfg.index(f"editor={editor}\n")] = f"editor={args.editor}\n"
        with open(cfgPath, 'w') as cfgFile:
            cfgFile.writelines(cfg)

    elif args.addRecovery:
        pass
    
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=DESCRIPTION
    )

    parser.add_argument('alias', nargs='?', help='Open a file by its alias.')
    parser.add_argument('--recover', metavar='ALIAS', help='Recover a file by its alias.')
    parser.add_argument('--auto-recovery', dest="autoRecovery", action='store_true', help='Back up files when adding them.')
    parser.add_argument('--add-open', dest="addOpen", type=str, metavar='PATH', help='Add a file to open by alias.')
    parser.add_argument('--alias', dest='newAlias', metavar='NAME', help='Alias for the file passed to --add-open.')
    parser.add_argument('--editor', metavar='NAME', help='Set the default editor.')
    parser.add_argument('--add-recovery', dest="addRecovery", metavar='PATH', help='Create a backup of a file.')
    parser.add_argument('--update', action='store_true', help="Update the recovery files.")
    parser.add_argument('--update-all', dest="updateAll", action='store_true', help="Update all recovery files.")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        print("I don't know what to do... there's no args.")
        sys.exit(1)
    
    if SUDO:
        if not os.path.exists("/etc/qktool/recovery.d"):
            os.makedirs("/etc/qktool/recovery.d")
    else:
        if not os.path.exists(f"/home/{USER}/qktool/recovery.d"):
            os.makedirs(f"/home/{USER}/qktool/recovery.d", exist_ok=True)
    
    main(args)