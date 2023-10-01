import sqlite3
from bs4 import BeautifulSoup

# Connect to SQLite Database and create a new table
conn = sqlite3.connect('papers.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS papers
             (title TEXT, abstract TEXT)''')

# Read and parse the HTML file
with open('all.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Find all the relevant blocks by looking for the <tr class="pHdr"> tags
blocks = soup.find_all('tr', class_='pHdr')

for block in blocks:
    try:
        # Find the title within the block
        title_tag = block.find_next('span', class_='pTtl')
        title = title_tag.get_text(strip=True)
        
        # Find the abstract within the block
        abstract_tag = block.find_next('td', colspan='2', style='padding: 0px')
        abstract = abstract_tag.div.get_text(strip=True)
        
        # Insert the title and abstract into the database
        c.execute("INSERT INTO papers (title, abstract) VALUES (?, ?)", (title, abstract))
    except Exception as e:
        print(f"Error processing block: {e}")

# Commit the changes and close the connection
conn.commit()
conn.close()
