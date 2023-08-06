# repeatexec

#### Description
run a command repeatedly.
```
repeatexec -n 10 -e ls
```
run `ls` every 10 seconds

#### changes

#### 0.0.7

when there are untract files, `isgitdirty` return true.

```python
def is_git_dirty():
    if has_change() or has_untracted_files():
        sys.exit(0)
    else:
        sys.exit(1)
```

##### 0.0.6
add command isgitdirty to check if current git repo is dirty.  
```bash
isgitdirty && echo dirty
```
The implementation is very simple:
```python
import sys
import subprocess
def is_git_dirty():
    result = subprocess.run(('git', 'diff', '--name-only'), capture_output=True)
    if result.stdout != b'':
        sys.exit(0)
    else:
        sys.exit(1)
```

##### 0.0.5
print current timestamp before running command

```python
def repeate_exec():
    if not option_check():
        return
    sec_i = sys.argv.index('-n') + 1
    cmd_i = sys.argv.index('-e') + 1
    sleep_seconds = int(sys.argv[sec_i])
    command = sys.argv[cmd_i:]
    command = ' '.join(command)
    print('commands:', command)
    print(f'interval: {sleep_seconds}s')
    while True:
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'----------------------------------------------------------------')
        print(f'                      {ts}                        ')
        print(f'----------------------------------------------------------------')
        run_command(command)
        time.sleep(sleep_seconds)
```