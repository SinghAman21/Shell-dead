import os
import threading
import time
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

# Set window size
Window.size = (400, 400)

class ShellApp(App):
    task_done = False

    def build(self):
        # Set the layout
        layout = BoxLayout(orientation='vertical', padding=10)

        # Set up a scrolling output area
        self.output = Label(size_hint_y=None, text_size=(380, None), halign="left", valign="top", color=(1, 1, 1, 1))
        self.output.bind(texture_size=self.output.setter('size'))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.output)

        # Input field for user commands
        self.input_field = TextInput(size_hint=(1, 0.2), multiline=False, background_color=(0, 0, 0, 1), foreground_color=(1, 1, 1, 1))
        self.input_field.bind(on_text_validate=self.on_enter)

        # Add components to the layout
        layout.add_widget(scroll)
        layout.add_widget(self.input_field)

        # Set background color
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background

        # Display initial working directory prompt
        self.update_output(os.getcwd() + "> ")

        return layout

    def on_enter(self, instance):
        user_input = self.input_field.text.strip()
        self.input_field.text = ""  # Clear the input field

        if user_input == "exit":
            self.stop()
            return

        if user_input.startswith("echo"):
            content = user_input.split(" ", 1)
            if len(content) > 1:
                self.update_output(content[1])
            else:
                self.update_output("")
            self.update_output(os.getcwd() + "> ")  # Add prompt after command execution
            return

        if user_input == "pwd":
            self.update_output(os.getcwd())
            self.update_output(os.getcwd() + "> ")  # Add prompt after command execution
            return

        if user_input.startswith("cd"):
            parts = user_input.split(" ", 1)
            if len(parts) > 1:
                path = parts[1].strip()
                try:
                    os.chdir(path)
                    self.update_output("Changed directory to: " + os.getcwd())
                except FileNotFoundError:
                    self.update_output(f"Directory '{path}' not found.")
            else:
                self.update_output("Usage: cd <directory>")
            self.update_output(os.getcwd() + "> ")  # Add prompt after command execution
            return

        if user_input == "ls":
            try:
                files = os.listdir(os.getcwd())
                self.update_output("\n".join(files))
            except Exception as e:
                self.update_output(str(e))
            self.update_output(os.getcwd() + "> ")  # Add prompt after command execution
            return

        if user_input.startswith("type"):
            cmd = user_input.split(" ")[1]
            self.search_command(cmd)
            return

        self.update_output(f"{user_input}: command not found")
        self.update_output(os.getcwd() + "> ")  # Add prompt after command execution

    def update_output(self, text):
        """Update the shell output area with new text."""
        self.output.text += text + "\n"
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.1)

    def scroll_to_bottom(self):
        """Ensure the scroll view is always at the bottom when new text is added."""
        self.output.parent.scroll_y = 0

    def search_command(self, cmd):
        """Search for a command in PATH."""
        def loader():
            loading = ['|', '/', '-', '\\']
            i = 0
            while not self.task_done:
                self.update_output(f'Searching {loading[i % len(loading)]}')
                i += 1
                time.sleep(0.1)

        self.task_done = False
        loader_thread = threading.Thread(target=loader)
        loader_thread.start()

        cmd_path = None
        try:
            PATH = os.environ.get("PATH", "")
            paths = PATH.split(";")
            root = paths[0][0:3]
            for root, dirs, files in os.walk(root):
                if cmd in files:
                    cmd_path = os.path.join(root, cmd)
                    break
        except Exception as e:
            cmd_path = None
            self.update_output(f"Error searching for command: {e}")
        finally:
            self.task_done = True
            loader_thread.join()

        if cmd_path:
            self.update_output(f"{cmd} is in {cmd_path}")
        else:
            self.update_output(f"'{cmd}' not found")

        self.update_output(os.getcwd() + "> ")  # Add prompt after command execution

if __name__ == '__main__':
    ShellApp().run()
