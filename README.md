# qktool
Commonly opened files opened up quick.
Also you can recover files.

If the file normally requires you to run with 'sudo', then you MUST run this in sudo.  
The opposite is also true. If user owns the file, then do NOT use sudo.

## Usage:
### qko
```
qk [alias]                                  # Open your file with the default editor.
qk -a [Path to file] --alias [alias] -r     # Add a new file to quickly open under an alias.
                                            # Optionally, create a backup.
qk --set-recovery                           # When adding a file to open, auto save a backup.
```

### qkr
```
qk [alias]                # Recover a previously backed up file.

qk --editor [Name of editor]        # Set the default editor.
qk --add [Path to file]    # Create a backup file stored by qktool.

# Add a file to quickly open under your chosen alias.
# Optionally, you can choose to add the file to recovery.

```

### qkcfg
```
qkcfg [Path to file] [variable name] [New value]
```