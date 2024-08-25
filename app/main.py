import sys


def main():
    # valid_command = ["exit 0"]
    
    # Uncomment this block to pass the first stage
    while True:
        sys.stdout.write("\u2620   ")
        sys.stdout.flush()
 
        # Wait for user input
        full_command = input()
        command_array = full_command.split()
        command = command_array[0]
        if command == "exit":
            break
        elif command == "echo":
            echo = ""
            for word in command_array[1:]:
                echo += f"{word} "
            print(echo.rstrip())
        elif command == "type":
            evaled_command = command_array[1]
            if evaled_command in ["echo", "exit", "type"]:
                print(f"{evaled_command} is a shell builtin")
            else:
                print(f"{evaled_command} not found")
        else:
            print(f"{command_array[0]}: command not found")

             
            # if user_command not in valid_command:
            #     sys.stdout.write(f"{user_command}: command not found\n")
            #     continue

            # if user_command == "exit 0":
            #     print("exit 0")
            #     break

if __name__ == "__main__":
    main()
