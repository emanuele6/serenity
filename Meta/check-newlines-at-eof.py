#!/bin/python3

import os
import subprocess
import sys

try:
    os.chdir(os.path.dirname(__file__) + "/..")
except:
    os.exit(1)

files = subprocess.run(
    [
        "git", "ls-files", "--",
        "*.cpp",
        "*.h",
        "*.gml",
        "*.html",
        "*.js",
        "*.css",
        "*.sh",
        "*.py",
        ":!:Base",
        ":!:Kernel/FileSystem/ext2_fs.h",
        ":!:Libraries/LibC/getopt.cpp",
        ":!:Libraries/LibCore/puff.h",
        ":!:Libraries/LibCore/puff.cpp",
        ":!:Libraries/LibELF/exec_elf.h"
    ],
    capture_output=True
).stdout.decode().split('\n')

MISSING_NEWLINE_AT_EOF_ERRORS = []
MORE_THAN_ONE_NEWLINE_AT_EOF_ERRORS = []

did_fail = False
for filename in files:
    try:
        f = open(filename, "r")
    except:
        continue

    f.seek(0, os.SEEK_END)

    f.seek(f.tell() - 1, os.SEEK_SET)
    if f.read(1) == '\n':
        while True:
            f.seek(f.tell() - 2, os.SEEK_SET)

            char = f.read(1)
            if not char.isspace():
                break
            if char == '\n':
                did_fail = True
                MORE_THAN_ONE_NEWLINE_AT_EOF_ERRORS.append(filename)
                break

        f.close()
        continue

    did_fail = True
    MISSING_NEWLINE_AT_EOF_ERRORS.append(filename)

    f.close()

if MISSING_NEWLINE_AT_EOF_ERRORS:
    print("Files with no newline at the end:", " ".join(MISSING_NEWLINE_AT_EOF_ERRORS))
if MORE_THAN_ONE_NEWLINE_AT_EOF_ERRORS:
    print("Files that have blank lines at the end:", " ".join(MORE_THAN_ONE_NEWLINE_AT_EOF_ERRORS))

if did_fail:
    sys.exit(1)
sys.exit(0)
