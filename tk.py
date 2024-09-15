import sys
import os
import threading
import time
import tkinter as tk
from tkinter import scrolledtext

task_done = False

# -------------- Utility Functions ----------------

def write_output(output_box, text):
    """Utility function to write output to the output_box and scroll to the bottom."""
    output_box.insert(tk.END, text + "\n")
    output_box.see(tk.END)
    output_box.update()

def loader(output_box):
    """Loader animation to show searching status."""
    loading = ['|', '/', '-', '\\']
    i = 0
    while not task_done:
        output_box.after(100, write_output, output_box, f'Searching {loading[i % len(loading)]}')
        i += 1
        time.sleep(0.1)

# -------------- Command Execution Functions ----------------

def handle_type(command, output_box):
    """Handles the 'type' command."""
    global task_done
    builtin_cmds = ["echo", "exit 0", "type", "cd", "pwd", "ls"]
    cmd = command.split(" ")[1]

    if cmd in builtin_cmds:
        write_output(output_box, f"{cmd} is a shell builtin")
    else:
        task_done = False
        loader_thread = threading.Thread(target=loader, args=(output_box,))
        loader_thread.start()

        # Start the search in a separate thread
        search_thread = threading.Thread(target=search_command, args=(cmd, output_box))
        search_thread.start()

def search_command(cmd, output_box):
    """Search for a command in the file system."""
    global task_done
    try:
        cmd_path = None
        PATH = os.environ.get("PATH")
        paths = PATH.split(";")
        root = paths[0][0:3]  # Get root drive (for Windows)
        for root, dirs, files in os.walk(root):
            if cmd in files:
                cmd_path = os.path.join(root, cmd)
                break
    except KeyboardInterrupt:
        output_box.after(100, write_output, output_box, "\nSearch interrupted by Keyboard.")
        cmd_path = None
    finally:
        task_done = True
        loader_thread.join()

    # Clear the line after search completes
    output_box.after(100, write_output, output_box, "\r" + " " * 20 + "\r")

    # Display search result in the main thread
    if cmd_path:
        output_box.after(100, write_output, output_box, f"{cmd} is in {cmd_path}")
    else:
        output_box.after(100, write_output, output_box, f"'{cmd}' not found")

# -------------- Event Handlers ----------------

def on_enter(event):
    """Handles the Return key press to execute a command."""
    command = entry.get().strip()
    write_output(output_box, os.getcwd() + "> " + command)
    entry.delete(0, tk.END)
    run_command(command, output_box)

# -------------- Command Dispatcher ----------------

def run_command(command, output_box):
    """Main command handler that decides which command function to call."""
    if command == "exit 0":
        write_output(output_box, "Exiting...")
        root.quit()

    elif command.startswith("echo"):
        handle_echo(command, output_box)

    elif command.startswith("type"):
        handle_type(command, output_box)

    elif command.startswith("cd"):
        handle_cd(command, output_box)

    elif command == "pwd":
        handle_pwd(output_box)

    elif command == "ls":
        handle_ls(output_box)

    else:
        write_output(output_box, f"{command}: command not found")

# -------------- GUI Setup ----------------

root = tk.Tk()
root.title("Shell Interface")

# Output box (for command output)
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=80)
output_box.pack(pady=10)

# Entry box (for command input)
entry = tk.Entry(root, width=80)
entry.pack()
entry.bind("<Return>", on_enter)

# Start the GUI event loop
root.mainloop()
