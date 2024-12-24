📱 Clariyo App
🚀 Overview
Clariyo is a safety-focused application built using Kivy to provide essential assistance in emergencies. It includes features like user registration, profile management, and an emergency alert system that sends alerts to guardians with location details.

🛠️ Features
📝 User Registration: Sign up with personal and guardian details.
🔒 Login System: Secure user authentication.
👤 Profile Management: View your profile with critical details.
🚨 Emergency Alerts: Send SMS alerts with location data to guardians.
🗺️ Location Sharing: Automatically fetch and share the user’s current location.
⚙️ Installation and Setup
Clone the repository:

bash
Copy code
git clone https://github.com/your-repo/clariyo-app.git
cd clariyo-app
Install dependencies:

bash
Copy code
pip install kivy twilio geocoder
Set up the database:
A SQLite database is automatically created during the first run.

Configure Twilio: Replace placeholders in the code with your Twilio credentials:

TWILIO_SID
TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER
Run the application:

bash
Copy code
python main.py
🧩 File Structure
main.py: Contains the core application logic.
db/clariyo.db: SQLite database for storing user data.
README.md: Documentation for the project.
🖥️ How to Use
Sign Up: Enter your name, email, medical condition, and guardian details.
Login: Use your email and password to access your profile.
Trigger Alert: Press the "Trigger Alert" button to send an emergency message to your guardian, including your current location.
🛡️ Tech Stack
Frontend: Kivy Framework
Backend: SQLite
API: Twilio for SMS
Location Services: Geocoder
🌟 Key Shortcuts
Ctrl + P: Instantly trigger an alert from anywhere in the app.
📸 Screenshots
🖊️ Sign-Up Page
🔒 Login Page
👤 Profile Page
🚨 Emergency Alert Trigger
📞 Emergency Alert Details
Guardian Name and Contact
User’s Current Location
💡 Future Enhancements
Add dark mode. 🌑
Include voice-activated emergency triggers. 🎤
Integrate with hospital databases for faster assistance. 🏥
💻 Contributing
Feel free to fork the repository and contribute! 😊

Happy Coding! ❤️



https://github.com/user-attachments/assets/141ca6fe-9ea5-4d9b-8dba-6a8b4d87ba1b







![clariyo-output(image)](https://github.com/user-attachments/assets/e31583b2-4fb5-49df-a0a6-1ff773701859)

