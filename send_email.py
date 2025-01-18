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
    today = datetime.now().strftime("%Y-%m-%d")
    for note in notes:
        if note.get('date') == today:
            return note
    return None

def format_email_content(note):
    email_content = f"""
    <h1>{note['title']}</h1>
    <h2>Question</h2>
    <p>{note.get('question', 'No question provided.')}</p>
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

    if note.get('example'):
        email_content += f"""
        <h2>Example</h2>
        <p><strong>Input:</strong> {note['example']['input']}</p>
        <p><strong>Output:</strong> {note['example']['output']}</p>
        """

    if note.get('link'):
        email_content +=f"""
        <h2>Reference Link</h2>
        <p><a href="{note['link']}">{note['link']}</a></p>
        """

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
    notes = load_notes(JSON_FILE_PATH)
    todays_note = find_todays_notes(notes)
    if todays_note:
        email_content = format_email_content(todays_note)
        send_email(f"DSA Notes: {todays_note['title']}", email_content)
        print("Email sent successfully!")
    else:
        print("No notes found.")

if __name__ == "__main__":
    main()
