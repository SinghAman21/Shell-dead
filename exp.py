import sys
import os
import threading
import time
import tkinter as tk
from tkinter import scrolledtext

task_done = False

def loader(output_box):
    loading = ['|', '/', '-', '\\']
    i = 0
    while not task_done:
        output_box.insert(tk.END, f'\rSearching {loading[i % len(loading)]}')
        output_box.see(tk.END)
        output_box.update()
        i += 1
        time.sleep(0.1)
    output_box.insert(tk.END, '\r')  # Clears the line

def run_command(cmd, output_box):
    global task_done
    builtin_cmds = ["echo", "exit 0", "type", "cd", "pwd", "ls"]
    PATH = os.environ.get("PATH")

    if cmd == "exit 0":
        output_box.insert(tk.END, "\nExiting...\n")
        output_box.see(tk.END)
        output_box.update()
        root.quit()

    elif cmd.startswith("echo"):
        content = cmd.split(" ", 1)
        if len(content) > 1:
            output_box.insert(tk.END, content[1] + "\n")
        else:
            output_box.insert(tk.END, "\n")
        output_box.see(tk.END)

    elif cmd.startswith("type"):
        user_input = cmd.split(" ")[1]
        if user_input in builtin_cmds:
            output_box.insert(tk.END, f"{user_input} is a shell builtin\n")
        else:
            task_done = False
            loader_thread = threading.Thread(target=loader, args=(output_box,))
            loader_thread.start()

            try:
                cmd_path = None
                paths = PATH.split(";")
                root_dir = paths[0][0:3]
                for root, dirs, files in os.walk(root_dir):
                    if user_input in files:
                        cmd_path = os.path.join(root, user_input)
                        break
            except KeyboardInterrupt:
                output_box.insert(tk.END, "\nSearch interrupted by Keyboard.\n")
                cmd_path = None
            finally:
                task_done = True
                loader_thread.join()

            output_box.insert(tk.END, "\r" + " " * 20 + "\r")  # Clears the line

            if cmd_path:
                output_box.insert(tk.END, f"{user_input} is in {cmd_path}\n")
            else:
                output_box.insert(tk.END, f"'{user_input}' not found\n")

        output_box.see(tk.END)

    elif cmd.startswith("cd"):
        parts = cmd.split(" ", 1)
        if len(parts) > 1:
            path = parts[1].strip()
            if path == "..":
                os.chdir(os.path.dirname(os.getcwd()))
            else:
                try:
                    os.chdir(path)
                except FileNotFoundError:
                    output_box.insert(tk.END, f"The path '{path}' does not exist.\n")
        else:
            output_box.insert(tk.END, "No path provided. Usage: cd <path>\n")
        output_box.see(tk.END)

    elif cmd == "pwd":
        output_box.insert(tk.END, "Current working directory: " + os.getcwd() + "\n")
        output_box.see(tk.END)

    elif cmd == "ls":
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                output_box.insert(tk.END, file + "\n")
        output_box.see(tk.END)

    else:
        output_box.insert(tk.END, f"{cmd}: command not found\n")
        output_box.see(tk.END)

def on_enter(event):
    command = entry.get().strip()
    output_box.insert(tk.END, os.getcwd() + "> " + command + "\n")
    entry.delete(0, tk.END)
    run_command(command, output_box)

# Create the main window
root = tk.Tk()
root.title("Dead's Shell")

# Output box (for command output)
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=80)
output_box.pack(pady=10)

# Entry box (for command input)
entry = tk.Entry(root, width=80)
entry.pack()
entry.bind("<Return>", on_enter)

# Start the GUI event loop
root.mainloop()
