import sys
import os
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")
    # Uncomment this block to pass the first stage
    # Wait for user input and print it back
    builtin_cmds = ["echo", "exit 0", "type"]
    PATH = os.environ.get("PATH")
    current_directory = os.getcwd()
    print("Current Directory:", current_directory)
    print("PATH:", PATH)
    while True:
        sys.stdout.write("$ ")
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
            cmd_path = None
            paths = PATH.split(":")
            for path in paths:
                if os.path.isfile(f"{path}/{cmd}"):
                    cmd_path = f"{path}/{cmd}"
            if cmd in builtin_cmds:
                sys.stdout.write(f"{cmd} is a shell builtin\n")
            elif cmd_path:
                sys.stdout.write(f"{cmd} is {cmd_path}\n")
            else:
                sys.stdout.write(f"{cmd} not found\n")
            sys.stdout.flush()
            continue
        sys.stdout.write(f"{user_input}: command not found\n")
        sys.stdout.flush()
if __name__ == "__main__":
    main()