# Shell-scripter, a shell scripting library for Python

**Shell-scripter is still a work-in-progress. API may change at any time.**

## Installation

Shell-scripter is on the Python Package Index and can be installed with `pip install shell-scripter`

## Example Usage

```python
from shell_scripter import run

run("cat", "logfile").pipe("grep", "error")().show()
```
