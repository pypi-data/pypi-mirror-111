import subprocess
import sys


def has_untracted_files():
    result = subprocess.run(('git', 'status'), capture_output=True)
    if b'Untracked files' in result.stdout:
        return True
    else:
        return False


def has_change():
    result = subprocess.run(('git', 'diff', '--name-only'), capture_output=True)
    if result.stdout != b'':
        return True
    else:
        return False


def is_git_dirty():
    if has_change() or has_untracted_files():
        sys.exit(0)
    else:
        sys.exit(1)
