# REPL on CLI

REPL extension to CLI apps

### Example

```python
import sys
from reploncli import reploncli

import my_cli_function, show_help

# turn on REPL mode if the first command line argument is 'repl'
lets_start_in_repl_mode = (sys.argv[1:] or [''])[0] == "repl"

reploncli(my_cli_function, lets_start_in_repl_mode, show_help, ">>> ")
```

### reploncli()

Signature:
```python
def reploncli(cli_function, repl_mode=None, help=None, prompt=""):
    ...
```

If `repl_mode is True` then REPL mode starts.

### Wrap your CLI entry point

Create `cli_function` by wrapping your CLI entry point that accepts one optional argument with `args` to use as a replacement for `sys.argv` if given.  
Otherwise process `sys.argv` as normal.

### Shell commands

If an input in REPL mode starts with `.` then it's run by `os.system()` after removing that dot.
