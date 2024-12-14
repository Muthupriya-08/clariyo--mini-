import os
import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from twilio.rest import Client
from kivy.core.window import Window
import geocoder

# Database Setup
DB_NAME = os.path.join("db", "clariyo.db")


def create_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT UNIQUE,
                        password TEXT,
                        medical_condition TEXT,
                        guardian_name TEXT,
                        guardian_contact TEXT
                    )''')
    conn.commit()
    conn.close()


create_db()

# Twilio Configuration
TWILIO_SID = "*******************************1"
TWILIO_AUTH_TOKEN = "***************************"
TWILIO_PHONE_NUMBER = "************"


class SignUpScreen(Screen):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.name_input = TextInput(hint_text="Enter Name")
        self.email_input = TextInput(hint_text="Enter Email")
        self.password_input = TextInput(hint_text="Enter Password", password=True)
        self.condition_input = TextInput(hint_text="Medical Condition")
        self.guardian_name_input = TextInput(hint_text="Guardian Name")
        self.guardian_contact_input = TextInput(hint_text="Guardian Contact (Phone Number)")

        layout.add_widget(Label(text="Sign Up"))
        layout.add_widget(self.name_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.condition_input)
        layout.add_widget(self.guardian_name_input)
        layout.add_widget(self.guardian_contact_input)

        sign_up_btn = Button(text="Sign Up")
        sign_up_btn.bind(on_press=self.sign_up)
        layout.add_widget(sign_up_btn)

        layout.add_widget(Button(text="Go to Login", on_press=self.go_to_login))
        self.add_widget(layout)

    def sign_up(self, instance):
        name = self.name_input.text
        email = self.email_input.text
        password = self.password_input.text
        condition = self.condition_input.text
        guardian_name = self.guardian_name_input.text
        guardian_contact = self.guardian_contact_input.text

        if not all([name, email, password, condition, guardian_name, guardian_contact]):
            self.show_popup("Error", "All fields are required!")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password, medical_condition, guardian_name, guardian_contact) VALUES (?, ?, ?, ?, ?, ?)",
                (name, email, password, condition, guardian_name, guardian_contact),
            )
            conn.commit()
            self.manager.current = 'login'
        except sqlite3.IntegrityError:
            self.show_popup("Error", "Email already exists!")
        finally:
            conn.close()

    def go_to_login(self, instance):
        self.manager.current = 'login'

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.5))
        popup.open()


class LoginScreen(Screen):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.email_input = TextInput(hint_text="Enter Email")
        self.password_input = TextInput(hint_text="Enter Password", password=True)
        layout.add_widget(Label(text="Login"))
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)

        login_btn = Button(text="Login")
        login_btn.bind(on_press=self.login)
        layout.add_widget(login_btn)

        sign_up_btn = Button(text="Sign Up")
        sign_up_btn.bind(on_press=self.go_to_signup)
        layout.add_widget(sign_up_btn)

        self.add_widget(layout)

    def login(self, instance):
        email = self.email_input.text
        password = self.password_input.text

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.manager.current_user = user
            self.manager.current = 'profile'
        else:
            self.show_popup("Error", "Invalid credentials")

    def go_to_signup(self, instance):
        self.manager.current = 'signup'

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.5))
        popup.open()


class ProfileScreen(Screen):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.populate_profile()

    def populate_profile(self):
        self.layout.clear_widgets()
        user = self.manager.current_user
        if user:
            self.layout.add_widget(Label(text=f"Name: {user[1]}"))
            self.layout.add_widget(Label(text=f"Medical Condition: {user[4]}"))
            self.layout.add_widget(Label(text=f"Guardian: {user[5]}"))
            self.layout.add_widget(Label(text=f"Guardian Number: {user[6]}"))

            trigger_btn = Button(text="Trigger Alert")
            trigger_btn.bind(on_press=self.trigger_alert)
            self.layout.add_widget(trigger_btn)

            logout_btn = Button(text="Logout")
            logout_btn.bind(on_press=self.logout)
            self.layout.add_widget(logout_btn)
        else:
            self.layout.add_widget(Label(text="No user data available."))

    def trigger_alert(self, instance):
        user = self.manager.current_user
        if user:
            guardian_contact = user[6]
            guardian_name = user[5]
            location = geocoder.ip('me')
            location_msg = f"Location: {location.latlng}" if location.latlng else "Location: Unknown"
            message_body = (
                f"🚨 Alert 🚨\n"
                f"Name: {user[1]} needs urgent help!\n\n"
                f"📍 Current Location: {location_msg}\n\n"
                "Please provide assistance immediately."
            )

            try:
                client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
                client.messages.create(
                    body=message_body,
                    from_=TWILIO_PHONE_NUMBER,
                    to=guardian_contact
                )
                self.show_popup("Success", f"Alert successfully sent to {guardian_name}!")
            except Exception as e:
                self.show_popup("Error", f"Failed to send alert: {str(e)}")

    def logout(self, instance):
        self.manager.current_user = None
        self.manager.current = 'login'

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.5))
        popup.open()


class ClariyoApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SignUpScreen(name='signup'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.current_user = None

        # Bind Ctrl + P key press to a function
        Window.bind(on_key_down=self.on_key_down)
        return sm

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        # Check if Ctrl + P is pressed
        if keycode == 44 and 'ctrl' in modifiers:  # 44 is the key code for 'P'
            profile_screen = self.root.get_screen('profile')
            if profile_screen:
                profile_screen.trigger_alert(None)  # Trigger the alert directly

if _name_ == '_main_':
    ClariyoApp().run()
