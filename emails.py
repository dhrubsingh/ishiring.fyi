import os
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
from scraper import scrape_page


urls = ['https://github.com/pittcsc/Summer2023-Internships','https://github.com/pittcsc/New-Grad-Positions-2023']
[data_internships, recent_internships] = scrape_page(urls[0], 'internships')
[data_newgrad, recent_newgrad] = scrape_page(urls[1], 'newgrad')


if recent_internships == [] and recent_newgrad == []:
    pass

else:
    db = sqlite3.connect('./data.db')
    recipients = db.execute('SELECT * from user_emails').fetchall()
    recipients = [str(row[0]) for row in recipients]

    sender = os.environ.get('EMAIL_ADDRESS')
    password = os.environ.get('EMAIL_PASSWORD')
    subject = 'ishiring.fyi - Recent Job Openings'
    email_body_html = ""
    email_body_text = ""
    for company in recent_internships:
        email_body_html += f"""
        <tr>
        <td><a href='{data_internships[company]['link']}'>{company}</a></td>
        <td>{data_internships[company]['location']}</td>
        <td>{data_internships[company]['notes']}</td>
        </tr>"""
        email_body_text += f"Company: {company} Location: {data_internships[company]['location']}  Note: {data_internships[company]['notes']} Link: {data_internships[company]['link']}\n"
    

    email_start_html = """
    <table>
    <thead>
    <tr>
    <th>Company</th>
    <th>Location</th>
    <th>Notes</th>
    </tr>
    </thead>
    <tbody>
    """

    email_start_text = "Company Location Notes Link\n"

    email_end_html = """
    </tbody>
    </table>
    """

    email_body_html = email_start_html + email_body_html + email_end_html
    email_body_text = email_start_text + email_body_text

    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['Subject'] = subject
    msg.attach(MIMEText(email_body_text, 'plain'))
    msg.attach(MIMEText(email_body_html, 'html'))
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        for recipient in recipients:
            msg['To'] = recipient
            smtp.sendmail(sender, recipient, msg.as_string())