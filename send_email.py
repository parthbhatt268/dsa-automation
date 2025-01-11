import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

JSON_FILE_PATH = 'notes.json'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = os.environ.get('SEMAIL')
EMAIL_PASSWORD = os.environ.get('PASS')
RECIPIENT_EMAIL = os.environ.get('REMAIL')

def load_notes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_todays_notes(notes):
    for note in notes:
        return note
    return None


def format_email_content(note):
    email_content = f"""
    <h1>{note['title']}</h1>
    <h2>DSA Solution</h2>
    <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 5px;">
{note['dsa_solution']}
    </pre>
    <h2>Notes</h2>
    <ul>
"""
    for line in note['notes']:
        email_content += f"<li>{line}</li>\n"
    email_content += "</ul>"
    return email_content

def send_email(subject, content):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'html'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

def main():
    # Debug: Print the environment variables to ensure they're being passed
    print(f"DUMMYSEMAIL: {EMAIL_ADDRESS}")  # Debug: Should print the sender email address
    print(f"DUMMYREMAIL: {RECIPIENT_EMAIL}")  # Debug: Should print the recipient email address
    print(f"DUMMYPASS: {EMAIL_PASSWORD}")  # Debug: Should print the email password (App Password)

    # Load the notes from the JSON file
    notes = load_notes(JSON_FILE_PATH)
    
    # Find today's note (or the first one for testing purposes)
    todays_note = find_todays_notes(notes)
    
    if todays_note:
        # Format the email content
        email_content = format_email_content(todays_note)
        
        # Send the email
        send_email(f"DSA Notes: {todays_note['title']}", email_content)
        print("Email sent successfully!")
    else:
        print("No notes found.")

if __name__ == "__main__":
    main()
