
# Shell Dead

Shell Dead is a terminal-based app that works like a standard terminal, allowing you to execute commands and perform tasks. It’s still in the development stage, with more features being added soon.







## Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 



## Features

- Command-line Interface (CLI) Simulation: Basic shell commands can be run, and the output is displayed in a console-like interface.
- Kivy-based GUI: A simple interface using Kivy with text input and output. **In-progress**
- Command Handler: The application processes commands entered by the user, managing file paths, directories, and simple command execution.
- Loader Animation: Simulates loading behavior when searching for a command (type command).
- Interrupt Handling: Gracefully handles keyboard interrupts.

## Dependencies
Python 3.x    
Kivy (GUI framework)  
`os`, `threading`, `time`, `sys` libraries (standard Python libraries)


## Supported Commands   

1. `echo <message`>:
Prints the <message> to the shell output.

Example: echo Hello World
Output: Hello World  
2. `exit 0`:
Exits the shell application.

Example: `exit 0`
Output: Exiting... (closes the shell)
3. `cd <path>`:
Changes the current directory to the specified <path>.

Example: `cd ..`
Output: Changes the directory to the parent directory.

Error Handling: If the provided path does not exist, an error message is displayed.  
4. `pwd`:
Prints the current working directory.

Example: `pwd`
Output: /home/user/shell (depending on the current directory)  
5. `ls`:
Lists the files in the current directory.

Example: `ls`
Output: Displays all files in the current working directory.  
6. `type <command>`:
Searches for the command in the system’s PATH directories. If the command exists, its location is displayed; otherwise, a "not found" message appears.

Example: `type` python
Output: python is in /usr/bin/python

Loader Animation: While searching, the shell shows a loading animation in the output box.

## PS: I am still working on this project, so there is plenty of room for additional features. Feel free to contribute by raising issues

### Thank you for reading
