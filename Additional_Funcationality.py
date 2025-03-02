import serial
import time
import os
import platform
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Serial Port Configuration
SERIAL_PORT = 'COM4'  # Change as per your system
BAUD_RATE = 9600

# Paths to video files
UNLOCK_VIDEO = "add Your path of Welcome.mp4"
LOCK_VIDEO = "add Your path of Lock.mp4"
WRONG_ATTEMPT_VIDEO = "add Your path of Access Denied.mp4"
FINAL_WARNING_VIDEO = "add Your path of 3 Time Wrong.mp4"

# Valid RFID Cards
VALID_CARDS = {"Card 1 ID", "Card 2 ID"}  #Add Your Card ID's
wrong_attempts = 0  

# Email Configuration
OWNER_EMAIL = "Example@gmail.com" #Add Owner Gmail ID 
SENDER_EMAIL = "Example@gmail.com" #Add Sender Gmail ID
SENDER_PASSWORD = "App Password"  #Add App Password of Gmail

def send_email():
    """Sends an email notification after 3 wrong attempts."""
    subject = "Security Alert: 3 Wrong RFID Attempts"
    body = "There have been 3 failed attempts to unlock the door. Please check the security system."
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = OWNER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, OWNER_EMAIL, msg.as_string())
        server.quit()
        print("📧 Security alert email sent successfully!")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

def play_video(file_path):
    """Plays the given video file depending on the OS."""
    if platform.system() == "Windows":
        os.system(f'start "" "{file_path}"')
    elif platform.system() == "Darwin":  
        os.system(f'open "{file_path}"')
    elif platform.system() == "Linux":
        os.system(f'xdg-open "{file_path}"')

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  

    print("✅ Listening for RFID scans...")

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()  
            line = ' '.join(line.split())  
            print(f"🔹 Raw Received: '{line}'")  

            if line in VALID_CARDS:
                print("🔓 Door Unlocked! Playing Unlock Video...")
                play_video(UNLOCK_VIDEO)
                wrong_attempts = 0  

            elif line == "PLAY_LOCK_VIDEO":
                print("🔒 Door Locked! Playing Lock Video...")
                play_video(LOCK_VIDEO)
                
            elif line == "WRONG_CARD":
                wrong_attempts += 1
                print(f"🚨 Wrong Card Attempt {wrong_attempts}!")
                play_video(WRONG_ATTEMPT_VIDEO if wrong_attempts < 3 else FINAL_WARNING_VIDEO)

                if wrong_attempts >= 3:
                    print("⚠ 3 Wrong Attempts! Sending Email Alert...")
                    send_email()
                    wrong_attempts = 0  

            else:
                print("⚠ Unrecognized input:", line)  

except serial.SerialException as e:
    print(f"❌ Serial Error: {e}")
    print("⚠ Make sure the Arduino is connected and the correct COM port is set.")

except KeyboardInterrupt:
    print("🔌 Script stopped by user.")
