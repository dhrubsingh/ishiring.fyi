from flask import Flask, render_template, request
from emails import companies, links, locations, notes
import re
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', companies=companies, 
        links=links, locations=locations, notes=notes, zip=zip               
)
    
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if (request.method == "POST"):
        user_email = request.form.get('user')
        if (check(user_email)):
            # Finish setting up alert in form.html
            db = sqlite3.connect('./data.db')
            cursor = db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS user_emails (emails TEXT NOT NULL)")

            
            cursor.execute("INSERT INTO user_emails (emails) VALUES (?)", user_email)
            db.commit()
            return render_template('form.html')
        else:
            return render_template('form.html', alert=True)
    else:
        return render_template('form.html')
    

def check(user):
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(email_format, user)):
        return True
    return False


if __name__ == "__main__":
    app.run(debug=True)

