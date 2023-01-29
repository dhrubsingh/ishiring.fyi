import requests
import json
from bs4 import BeautifulSoup

urls = ['https://github.com/pittcsc/Summer2023-Internships','https://github.com/pittcsc/New-Grad-Positions-2023']

def scrape_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    td_elements = soup.find_all('td')

    # create a dictionary that records links for any keyword
    # get link from company name, if that doesn't exist get link from first note
    # if that doesn't exist, get it from the location
    links = {}
    data = []

    for i in range(0, len(td_elements), 3):
        # filter out for any jobs that are still closed
        name = td_elements[i]
        location = td_elements[i + 1]
        notes = td_elements[i + 2]

        if "Closed" not in location.get_text() and "Closed" not in notes.get_text():
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
            
            data.append({
                "company": name.get_text(),
                "link": links[name.get_text()],
                "location": location.get_text(),
                "notes": notes.get_text()
            })

    jsonify = json.dumps(data)
    return jsonify

# convert list of dictionaries into a JSON file
internships = scrape_page(urls[0])

with open("internships.json", "w") as outfile:
    outfile.write(internships)

new_grad = scrape_page(urls[1])
with open("newgrad.json", "w") as outfile:
    outfile.write(new_grad)

       

