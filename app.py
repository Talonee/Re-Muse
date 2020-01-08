import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import socket_client
import os
import sys


class ReMuse(App):
    def build(self):
        # Manage and switch between screens
        self.screen_manager = ScreenManager()

        # Add Welcome and Browsing screen 
        self.welcome_page = WelcomePage()
        screen = Screen(name="Welcome")
        screen.add_widget(self.welcome_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

    # Add Progress screen
    def create_progress_page(self):
        self.progress_page = ProgressPage()
        screen = Screen(name="Progress")
        screen.add_widget(self.progress_page)
        self.screen_manager.add_widget(screen)

    # Add Review screen
    def create_review_page(self):
        self.review_page = ReviewPage()
        screen = Screen(name="Review")
        screen.add_widget(self.review_page)
        self.screen_manager.add_widget(screen)


class WelcomePage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2 # create 2 cols (description + text input)

        # Read in previous detail
        if os.path.isfile("prev_details.txt"):
            with open("prev_details.txt", "r") as f:
                d = f.read().split(",")
                prev_ip = d[0]
                prev_port = d[1]
                prev_username = d[2]
        else:
            prev_ip = ""
            prev_port = ""
            prev_username = ""

        # Add widgets to the Connect page
        self.add_widget(Label(text="IP:"))
        self.ip = TextInput(text=prev_ip, multiline=False)
        self.add_widget(self.ip)

        self.add_widget(Label(text="Port:"))
        self.port = TextInput(text=prev_port,multiline=False)
        self.add_widget(self.port)

        self.add_widget(Label(text="Username:"))
        self.username = TextInput(text=prev_username, multiline=False)
        self.add_widget(self.username)

        # Add "Join" button and bind action
        self.join = Button(text="Join")
        self.join.bind(on_press=self.join_button)
        self.add_widget(Label())
        self.add_widget(self.join)

    # Display user info and indicate connection attempt
    def join_button(self, instance):
        port = self.port.text
        ip = self.ip.text
        username = self.username.text

        with open("prev_details.txt", "w") as f:
            f.write(f"{ip},{port},{username}")
        
        info = f"Attempting to join {ip}:{port} as {username}"
        chat_app.info_page.update_info(info)

        chat_app.screen_manager.current = "Info" # Switch to Info screen
        Clock.schedule_once(self.connect, 1) # Connect

    # Connect to socket server
    def connect(self, _):
        # Get info for sockets client
        port = int(self.port.text)
        ip = self.ip.text
        username = self.username.text

        if not socket_client.connect(ip, port, username, show_error):
            return

        # Create chat page and switch
        chat_app.create_chat_page()
        chat_app.screen_manager.current = "Chat"


class ProgressPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1 

        # Display message to the center
        self.message = Label(halign="center", valign="middle", font_size=30)
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)

    # Display info/error message
    def update_info(self, message):
        self.message.text = message
    
    # Scale text to take up 90% of page's width
    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)


class ChatPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1 
        self.rows = 2

        # Add chat layout (ScrollableLabel enables flexbile layout scaling)
        # Chat layout takes up 90% of app's height
        self.history = ScrollableLabel(height=Window.size[1]*0.9, size_hint_y=None)
        self.add_widget(self.history)

        # Add widget for text input and send button
        # Text input takes up 80% of app's width
        self.new_message = TextInput(width=Window.size[0]*0.8, size_hint_x=None, multiline=False)
        self.send = Button(text="Send")
        self.send.bind(on_press=self.send_message)

        # Create 2 columns and insert "New Message" and "Send" widgets
        bottom_line = GridLayout(cols=2)
        bottom_line.add_widget(self.new_message)
        bottom_line.add_widget(self.send)
        self.add_widget(bottom_line)

        Window.bind(on_key_down=self.on_key_down) # send msg using Enter

        # Focus text input and listen to incoming msg
        Clock.schedule_once(self.focus_text_input, 1)
        socket_client.start_listening(self.incoming_message, show_error)
        self.bind(size=self.adjust_fields)

    # Updates page layout
    def adjust_fields(self, *_):

        # Chat history height - 90%, but at least 50px for bottom new message/send button part
        if Window.size[1] * 0.1 < 50:
            new_height = Window.size[1] - 50
        else:
            new_height = Window.size[1] * 0.9
        self.history.height = new_height

        # New message input width - 80%, but at least 160px for send button
        if Window.size[0] * 0.2 < 160:
            new_width = Window.size[0] - 160
        else:
            new_width = Window.size[0] * 0.8
        self.new_message.width = new_width

        # Update chat history layout
        #self.history.update_chat_history_layout()
        Clock.schedule_once(self.history.update_chat_history_layout, 0.01)

    # Get called on key press
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40: # Enter key
            self.send_message(None)

    def send_message(self, _):
        # Get msg text and clear msg input field
        message = self.new_message.text
        self.new_message.text = ""

        # Add msg to chat history and send to server
        if message:
            self.history.update_chat_history(f"[color=ff3399]{chat_app.connect_page.username.text}[/color] > {message}")
            socket_client.send(message)
        
        # Schedule a refocus to text input
        Clock.schedule_once(self.focus_text_input, 0.1)

    def focus_text_input(self, _):
        self.new_message.focus = True
    
    def incoming_message(self, username, message):
        self.history.update_chat_history(f"[color=00ffcc]{username}[/color] > {message}")


class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        # Allow text colors and artificial scrolling to 
        # ensure new messages are always visible
        self.chat_history = Label(size_hint_y=None, markup=True)
        self.scroll_to_point = Label()

        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)

    # Add new message to the chat history
    def update_chat_history(self, message):
        self.chat_history.text += '\n' + message

        # Set initial chat layout with font size, textbox width and height
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width*0.98, None)

        self.scroll_to(self.scroll_to_point)

    # Update chat layout
    def update_chat_history_layout(self, _=None):
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)


def show_error(message):
    chat_app.info_page.update_info(message)
    chat_app.screen_manager.current = "Info"
    Clock.schedule_once(sys.exit, 10)


if __name__ == "__main__":
    remuse = ReMuse()
    remuse.run()