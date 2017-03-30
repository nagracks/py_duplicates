#!/usr/bin/env python3

import subprocess

CMD = "./py_duplicates.py dir1 dir2"
EXPECTED_RETURN = """Duplicate Files => dir1/c, dir2/b
Duplicate Files => dir1/b, dir1/a
"""
ACTUAL_RETURN = subprocess.check_output(CMD, shell=True).decode()

if ACTUAL_RETURN == EXPECTED_RETURN:
    print("OK")
else:
    print("FAIL")
    print("actual_return is:\n"+ACTUAL_RETURN)
