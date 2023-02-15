import requests
from bs4 import BeautifulSoup
import sqlite3

db = sqlite3.connect("data.db")
cur = db.cursor()
urls = ['https://github.com/pittcsc/Summer2023-Internships','https://github.com/pittcsc/New-Grad-Positions-2023']

def scrape_page(url, position):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    td_elements = soup.find_all('td')

    relations = {
        "newgrad":"new_newgrad",
        "internships": "new_internships",
    }

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
            
    # modifying database

    comps = cur.execute(f"SELECT company from {position}").fetchall()
    companies = [str(row[0]) for row in comps]
    
    # delete any things in the table that isn't in the scraped data
    for company in companies:
        if company not in data:
            cur.execute(f"DELETE FROM {position} WHERE company = ?", (company,))
            # delete from most recent job postings
            cur.execute(f"DELETE FROM {relations[position]} WHERE company = ?", (company,))
            db.commit()
    
    # add any thing that is in the data table but not in the SQL table
    new_companies = []
    for i, entry in enumerate(data.keys()):
        if entry not in companies:
             new_companies.append(entry)
             #print(i, entry, data[entry]["link"], data[entry]["location"], data[entry]["notes"])
             cur.execute(f"INSERT INTO {position} (id, company, link, location, notes) VALUES (?, ?, ?, ?, ?)", (i, entry, data[entry]["link"], data[entry]["location"], data[entry]["notes"]))
             cur.execute(f"INSERT INTO {relations[position]} (id, company, link, location, notes) VALUES (?, ?, ?, ?, ?)", (i, entry, data[entry]["link"], data[entry]["location"], data[entry]["notes"]))
             db.commit()

    return [data, new_companies]

   

internships = scrape_page(urls[0], "internships")[0]
newgrad = scrape_page(urls[1], "newgrad")[0]



