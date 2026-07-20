# PysCLI

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Version](https://img.shields.io/badge/Version-v0.6-orange.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-success)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)
![Course](https://img.shields.io/badge/Course-Operating%20System-blueviolet)

**PysCLI** (Python Simple Command Line Interface) is a lightweight Unix-like shell implemented in Python. The project was developed as an educational operating systems project to demonstrate how a command-line interpreter works internally, from reading user input to parsing commands and executing processes.

PysCLI implements many of the core mechanisms of a shell, including a REPL, command parsing, built-in commands, external command execution, piping, input/output redirection, and debugging utilities.

---

## Features

### Interactive REPL

* Interactive shell prompt
* Continuous command execution loop
* Graceful exit handling

### Command Parsing

* Tokenization of user input
* Argument parsing
* Command validation
* Detection of pipes and redirections

### Built-in Commands

* `cd` — Change current working directory
* `pwd` — Print current working directory
* `help` — Display available commands
* `pyscli --version` — Display current version
* `debug --enable` — Enable debug mode
* `debug --disable` — Disable debug mode
* `exit` — Exit PysCLI

### External Command Execution

* Execute system commands
* Automatic PATH lookup
* Cross-platform implementation
* POSIX execution using `fork()` and `execvp()`
* Windows execution using `subprocess`

### Pipe Support

Supports Unix-style pipelines.


### Debug Mode

Debug mode displays internal shell information such as:

* Parsed tokens
* Command
* Arguments
* Execution flow

Useful for understanding how the shell processes commands.

---

# Project Structure

```
PySCLI/
│
├── main.py
├── parser.py
├── executor.py
├── commands.py
├── config.py
└── README.md
```

---

# Requirements

## Python

Python **3.10** or newer is recommended.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Dhimasekaputraa/pyscli.git
```

Move into the project directory:

```bash
cd pyscli
```

Run the shell:

Linux

```bash
python3 main.py
```

Windows

```powershell
python main.py
```

---

# Project Milestones

This project was created to explore the internal implementation of a command-line shell, including:

* REPL architecture
* Command parsing
* Process creation
* Inter-process communication (pipes)
* Input/output redirection
* Built-in command implementation
* Cross-platform process execution

---

# Author
<a href="https://github.com/Dhimasekaputraa/pyscli/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Dhimasekaputraa/pyscli" />
</a><br>
Developed as part of an Operating Systems course project.
Contributions, suggestions, and improvements are welcome.
