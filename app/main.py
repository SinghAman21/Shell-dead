import sys
import time
import threading
import os

task_done = False
def loader():
    loading = ['|', '/', '-', '\\']
    i = 0
    while not task_done:
        sys.stdout.write(f'\rSearching {loading[i % len(loading)]}')
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    sys.stdout.write('\r')  # Clears the line

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")
    # Uncomment this block to pass the first stage
    # Wait for user input and print it back
    builtin_cmds = ["echo", "exit 0", "type", "cd", "pwd", "ls"]
    PATH = os.environ.get("PATH")
    # current_directory = os.getcwd()
    # print("Your Current Working is Directory:", current_directory)
    # print("Your Current Working is Directory:", current_directory)

    # print("PATH:", PATH)
    while True:
        try:
            sys.stdout.write(os.getcwd() + "> "   u"\U0001F47E  ")
            sys.stdout.flush()
            user_input = input()
            if user_input == "exit 0":
                break

            if user_input.startswith("echo"):
                content = user_input.split(" ", 1)
                if len(content) > 1:
                    sys.stdout.write(content[1] + "\n")
                else:
                    sys.stdout.write("\n")
                sys.stdout.flush()
                continue

            if user_input.startswith("type"):
                cmd = user_input.split(" ")[1]
                if cmd in builtin_cmds:
                    sys.stdout.write(f"{cmd} is a shell builtin\n")
                    sys.stdout.flush()
                    continue

                global task_done
                task_done = False

                loader_thread = threading.Thread(target=loader)
                loader_thread.start()

                try:
                    cmd_path = None
                    paths = PATH.split(";")
                    root = paths[0][0:3]
                    for root, dirs, files in os.walk(root):
                        if cmd in files:
                            cmd_path = os.path.join(root, cmd)
                            break
                except KeyboardInterrupt:
                    sys.stdout.write("\nSearch interrupted by Keyboard.\n")
                    cmd_path = None
                finally:
                    task_done = True
                    loader_thread.join()

                sys.stdout.write("\r" + " " * 20 + "\r")  # Clears the line

                if cmd_path:
                    sys.stdout.write(f"{cmd} is in {cmd_path}\n")
                else:
                    sys.stdout.write(f"'{cmd}' not found\n")
                sys.stdout.flush()
                continue

            if user_input.startswith("cd"):
                parts = user_input.split(" ", 1)  # Split only once to avoid IndexError
                if len(parts) > 1:
                    path = parts[1].strip()  # Get the path part and remove any leading/trailing whitespace
                    if path == "..":
                        os.chdir(os.path.dirname(os.getcwd()))
                    else:
                        try:
                            os.chdir(path)
                        except FileNotFoundError:
                            print(f"The path '{path}' does not exist.")
                else:
                    print("No path provided. Usage: cd <path>")

            if user_input == "pwd":
                print("Current working directory: " + os.getcwd())

            if user_input == "ls":
                for root, dirs, files in os.walk(os.getcwd()):
                    for file in files:
                        print(file)

            if not any(user_input.startswith(cmd) for cmd in builtin_cmds):
                sys.stdout.write(f"{user_input}: command not found\n")
                sys.stdout.flush()
            
            if user_input == "dwn":
                pass

        except KeyboardInterrupt:
            sys.stdout.write("\nKeyboard Interrupt. Exiting...\n")
            break  # Exit the loop when Ctrl+C is pressed


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write("\nProgram interrupted. Exiting...\n")
        sys.exit(0)
