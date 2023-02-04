import requests
import json
from bs4 import BeautifulSoup
import sqlite3

db = sqlite3.connect("data.db")
cur = db.cursor()
urls = ['https://github.com/pittcsc/Summer2023-Internships','https://github.com/pittcsc/New-Grad-Positions-2023']

def scrape_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    td_elements = soup.find_all('td')

    # create a dictionary that records links for any keyword
    # get link from company name, if that doesn't exist get link from first note
    # if that doesn't exist, get it from the location
    links = {}
    data = {}

    for i in range(0, len(td_elements), 3):
        # filter out for any jobs that are still closed
        name = td_elements[i]
        location = td_elements[i + 1]
        notes = td_elements[i + 2]

        if "closed" not in location.get_text().lower() and "closed" not in notes.get_text().lower():
            # check if name has link
            if name.find('a') is not None:
                a_tag = name.find('a')
                link = a_tag.get('href')
                links[name.get_text()] = link
            elif location.find('a') is not None:
                a_tag = location.find('a')
                link = a_tag.get('href')
                links[name.get_text()] = link
            elif notes.find('a') is not None:
                a_tag = notes.find('a')
                link = a_tag.get('href')
                links[name.get_text()] = link
            else:
                continue

            # check if location has link
            # check if notes has link
            data[name.get_text()] = {
                "link": links[name.get_text()],
                "location": location.get_text(),
                "notes": notes.get_text()
            }
            
            """
            data.append({
                "company": name.get_text(),
                "link": links[name.get_text()],
                "location": location.get_text(),
                "notes": notes.get_text()
            })
            """

    # instert/update database with information 

    """# approach 1: delete database, repopulate with newly scraped links
    cur.execute("DELETE from internships")
    db.commit()

    for i in range(len(data)):
        cur.execute("INSERT INTO internships (id, company, link, location, notes) VALUES (?, ?, ?, ?, ?)", (i, data[i]["company"], data[i]["link"], data[i]["location"], data[i]["notes"]))
        db.commit()
    """

    # approach 2: modifying database
    
    comps = cur.execute("SELECT company from internships").fetchall()
    companies = [str(row[0]) for row in comps]
    
    # delete any things in the table that isn't in the scraped data
    for company in companies:
        if company not in data:
            cur.execute("DELETE FROM internships WHERE company = ?", (company,))
            db.commit()
    
    # add any thing that is in the data table but not in the SQL table
    for i, entry in enumerate(data.keys()):
        if entry not in companies:
             #print(i, entry, data[entry]["link"], data[entry]["location"], data[entry]["notes"])
             cur.execute("INSERT INTO internships (id, company, link, location, notes) VALUES (?, ?, ?, ?, ?)", (i, entry, data[entry]["link"], data[entry]["location"], data[entry]["notes"]))
             db.commit()

    #print(data)

    return data

    """
    jsonify = json.dumps(data)
    return jsonify
    """

internships = scrape_page(urls[0])

"""
# convert list of dictionaries into a JSON file
internships = scrape_page(urls[0])

with open("internships.json", "w") as outfile:
    outfile.write(internships)

new_grad = scrape_page(urls[1])
with open("newgrad.json", "w") as outfile:
    outfile.write(new_grad)
"""
       

