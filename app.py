from flask import Flask, render_template, request
from load_stored_data import internships_companies, internships_links, internships_locations, internships_notes
from load_stored_data import newgrad_companies, newgrad_links, newgrad_locations, newgrad_notes
import re
import sqlite3

app = Flask(__name__)



@app.route('/', methods=["GET", "POST"])
def index():
    if (request.method == "POST"):
        search_term = request.form.get('search-term').lower()
        if search_term == "":
            return render_template('index.html', companies=internships_companies, 
            links=internships_links, locations=internships_locations, notes=internships_notes, zip=zip)
        else:
            # SubSet lists
            company_ss, links_ss, locations_ss, notes_ss = [[] for _ in range(4)]
            for company, link, location, note in zip(internships_companies, internships_links, 
                internships_locations, internships_notes):
                if (search_term in company.lower()) or (search_term in link.lower()) or (search_term in location.lower()) or (search_term in note.lower()):
                    company_ss.append(company)
                    locations_ss.append(location)
                    links_ss.append(link)
                    notes_ss.append(note)
            return render_template('index.html', companies=company_ss, links=links_ss, 
                locations=locations_ss, notes=notes_ss, zip=zip)

    else:
        return render_template('index.html', companies=internships_companies, 
        links=internships_links, locations=internships_locations, notes=internships_notes, zip=zip               
)

@app.route('/newgrad', methods=["GET", "POST"])
def newgrad():
    if (request.method == "POST"):
        search_term = request.form.get('search-term').lower()
        if search_term == "":
            return render_template('newgrad.html', companies=newgrad_companies, 
            links=newgrad_links, locations=newgrad_locations, notes=newgrad_notes, zip=zip)
        else:
            # SubSet lists
            company_ss, links_ss, locations_ss, notes_ss = [[] for _ in range(4)]
            for company, link, location, note in zip(newgrad_companies, newgrad_links, 
                newgrad_locations, newgrad_notes):
                if (search_term in company.lower()) or (search_term in link.lower()) or (search_term in location.lower()) or (search_term in note.lower()):
                    company_ss.append(company)
                    locations_ss.append(location)
                    links_ss.append(link)
                    notes_ss.append(note)
            return render_template('newgrad.html', companies=company_ss, links=links_ss, 
                locations=locations_ss, notes=notes_ss, zip=zip)
    
    else:
        return render_template('newgrad.html', companies=newgrad_companies, 
        links=newgrad_links, locations=newgrad_locations, notes=newgrad_notes, zip=zip               
)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if (request.method == "POST"):
        user_email = request.form.get('user')
        if (check_email_format(user_email)):
            # Finish setting up alert in form.html
            db = sqlite3.connect('./data.db')
            cursor = db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS user_emails (emails TEXT NOT NULL)")

            email_data = cursor.execute("SELECT emails from user_emails").fetchall()
            email_data = [str(row[0]) for row in email_data]
            if (user_email in email_data):
                db.commit()
                return render_template('form.html', exists=True)

            else:
                cursor.execute("INSERT INTO user_emails (emails) VALUES (?)", (user_email,))
                db.commit()
                return render_template('form.html', success=True)
        else:
            return render_template('form.html', alert=True)
    else:
        return render_template('form.html')
    

def check_email_format(user):
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(email_format, user)):
        return True
    return False


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=8000)

