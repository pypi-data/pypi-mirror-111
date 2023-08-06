import subprocess
import os
import enum
import sys

class Pipe(enum.Enum):
    NULL=0
    STDOUT=1
    STDERR=2
    CPTOUT=3


class Command:
    def __init__(self, command, stdout, stderr, pre_command=None) -> None:
        self.command = command
        self.pre_command: Command = pre_command
        self.process = None
        self.env_vars = os.environ.copy()

        if stdout == Pipe.NULL:
            self.stdout = subprocess.NULL
        elif stdout == Pipe.STDOUT:
            self.stdout = sys.stdout
        elif stdout == Pipe.STDERR:
            self.stdout = sys.stderr
        elif stdout == Pipe.CPTOUT:
            self.stdout = subprocess.PIPE
        else:
            # Assume stdout is a file-like object
            self.stdout = stdout
        
        if stderr == Pipe.NULL:
            self.stderr = subprocess.NULL
        elif stderr == Pipe.STDOUT:
            self.stderr = sys.stdout
        elif stderr == Pipe.STDERR:
            self.stderr = sys.stderr
        elif stderr == Pipe.CPTOUT:
            self.stderr = subprocess.STDOUT
        else:
            # Assume stderr is a file-like object
            self.stderr = stderr

    def pipe(self, *command, stdout=Pipe.CPTOUT, stderr=Pipe.STDERR):
        return Command(command, stdout, stderr, self)

    def env(self, **vars):
        self.env_vars.update(vars)
        return self

    def _execute(self):
        if self.pre_command is not None:
            self.pre_command._execute()
            self.process = subprocess.Popen(
                self.command, stdin=self.pre_command.process.stdout,
                stdout=self.stdout, stderr=self.stderr, env=self.env_vars
            )
        else:
            self.process = subprocess.Popen(
                self.command, stdout=self.stdout, stderr=self.stderr,
                env=self.env_vars
            )

    def wait(self):
        if self.pre_command is not None:
            self.pre_command.wait()
        self.process.wait()

    def __call__(self, wait=True, *args, **kwds):
        self._execute()
        if wait:
            self.wait()
        return self
    
    def show(self):
        print(self.process.stdout.read().decode(), end="")
        return self


def run(*command, stdout=Pipe.CPTOUT, stderr=Pipe.STDERR):
    return Command(command, stdout, stderr)
