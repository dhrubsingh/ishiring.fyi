import sqlite3

# INTERNSHIPS

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