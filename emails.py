import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import sqlite3
import flask

# emails = ['tempestly18@gmail.com']
# sender_email = "ndatar18@gmail.com"

# for email in emails:
#     receiver_email = email
#     password = input("Type your password and press enter:")

#     message = MIMEMultipart("alternative")
#     message["Subject"] = "multipart test"
#     message["From"] = sender_email
#     message["To"] = receiver_email

#     # Create the plain-text and HTML version of your message
    # text = """\
    #     Hi,
    #     How are you?
    #     Real Python has many great tutorials:
    #     www.realpython.com"""
html = """\
    <html>
    <body>
        <p>Hi,<br>
        How are you?<br>
        <a href="http://www.realpython.com">Real Python</a> 
        has many great tutorials.
        </p>
    </body>
    </html>
    """

#     # Turn these into plain/html MIMEText objects
#     part1 = MIMEText(text, "plain")
#     part2 = MIMEText(html, "html")

#     # Add HTML/plain-text parts to MIMEMultipart message
#     # The email client will try to render the last part first
#     message.attach(part1)
#     message.attach(part2)

#     # Create secure connection with server and send email
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#         server.login(sender_email, password)
#         server.sendmail(
#             sender_email, receiver_email, message.as_string()
#         )
# with open('./internships.json') as file:
#     internships_data = json.load(file)

db = sqlite3.connect('./data.db')
data = db.execute("SELECT * FROM internships")
data = data.fetchall()

internships_companies = []
internships_links = []
internships_locations = []
internships_notes = []

for item in data:
    internships_companies.append(item[1])
    internships_links.append(item[2])
    internships_locations.append(item[3])

    if len(item[4]) < 125:
        internships_notes.append(item[4])
    else:
        internships_notes.append("Software Engineer Intern")


# NEW GRAD

data = db.execute("SELECT * FROM newgrad")
data = data.fetchall()

newgrad_companies = []
newgrad_links = []
newgrad_locations = []
newgrad_notes = []

for item in data:
    newgrad_companies.append(item[1])
    newgrad_links.append(item[2])
    newgrad_locations.append(item[3])
    if len(item[4]) < 110:
        newgrad_notes.append(item[4])
    else:
        newgrad_notes.append("Graduate Software Engineer")