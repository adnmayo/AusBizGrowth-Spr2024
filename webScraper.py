import requests
import csv
from bs4 import BeautifulSoup
import time
import chardet
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

def detectEncoding(filePath):
    with open(filePath, 'rb') as file:
        raw = file.read()
    return chardet.detect(raw)['encoding']

def getSMES(filePath):
    companies = []
    encoding = detectEncoding(filePath)
    with open(filePath, newline='', encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            companies.append(row)
    
    return companies

def scrapeNews(company):
    try:
        searchTerm = quote_plus(company['Company'])
        url = f"https://news.google.com/rss/search?q={searchTerm}"
        
        response = requests.get(url)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        newsResults = []
        for item in root.findall(".//item"):
            link = item.find("link").text
            newsResults.append(link)
        
        return newsResults

    except Exception as e:
        print(f"Error while scraping news for {company['Company']}: {e}")
        return []
  
def main():
    companies = getSMES('smelist.csv')
    
    for company in companies:
        print(f"Searching news for {company['Company']}...")
        companyResults = scrapeNews(company)
        
        print(f"Company: {company['Company']}")
        print("Article Links:")
        for link in companyResults:
            print(f"- {link}")
        print("---")
        
        time.sleep(1)
            
if __name__ == "__main__":
    main()
