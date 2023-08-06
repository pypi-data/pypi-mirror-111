import subprocess
import sys


def is_git_dirty():
    result = subprocess.run(('git', 'diff', '--name-only'), capture_output=True)
    if result.stdout != b'':
        sys.exit(0)
    else:
        sys.exit(1)
