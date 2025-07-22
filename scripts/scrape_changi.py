import os
import requests
from bs4 import BeautifulSoup
import time

def scrape_changi(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract paragraphs with meaningful content
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 50]
    
    # Extract headings with their content to maintain context
    headings = []
    for h in soup.find_all(['h1', 'h2', 'h3', 'h4']):
        heading_text = h.get_text(strip=True)
        if heading_text and len(heading_text) > 3:  # Avoid empty or very short headings
            headings.append(heading_text)
    
    # Extract list items which often contain important information
    list_items = [li.get_text(strip=True) for li in soup.find_all('li') if len(li.get_text(strip=True)) > 30]
    
    # Combine all extracted text
    all_text = paragraphs + headings + list_items
    return all_text

def save_data():
    # Ensure the directory exists
    os.makedirs("data", exist_ok=True)
    
    # Main URLs
    changi_url = "https://www.changiairport.com/"
    jewel_url = "https://www.jewelchangiairport.com/"
    
    # Additional specific URLs for more detailed information
    terminal_urls = [
        "https://www.changiairport.com/en/airport-guide/terminal-1.html",
        "https://www.changiairport.com/en/airport-guide/terminal-2.html",
        "https://www.changiairport.com/en/airport-guide/terminal-3.html",
        "https://www.changiairport.com/en/airport-guide/terminal-4.html",  # Specifically include T4
    ]
    
    facilities_urls = [
        "https://www.changiairport.com/en/airport-guide/facilities-and-services.html",
        "https://www.changiairport.com/en/airport-guide/transit-and-transfer.html",
        "https://www.changiairport.com/en/shop.html",
        "https://www.changiairport.com/en/dine.html"
    ]
    
    # Scrape main sites
    print("Scraping main Changi Airport website...")
    changi = scrape_changi(changi_url)
    
    print("Scraping Jewel website...")
    jewel = scrape_changi(jewel_url)
    
    # Scrape terminal-specific pages
    terminal_data = []
    for url in terminal_urls:
        print(f"Scraping {url}...")
        terminal_data.extend(scrape_changi(url))
        time.sleep(1)  # Be polite to the server
    
    # Scrape facilities pages
    facilities_data = []
    for url in facilities_urls:
        print(f"Scraping {url}...")
        facilities_data.extend(scrape_changi(url))
        time.sleep(1)  # Be polite to the server
    
    # Combine all data
    all_data = changi + jewel + terminal_data + facilities_data
    
    # Remove duplicates while preserving order
    unique_data = []
    seen = set()
    for item in all_data:
        if item not in seen:
            seen.add(item)
            unique_data.append(item)
    
    print(f"Total unique information snippets: {len(unique_data)}")
    
    # Write to file
    with open("data/changi_jewel.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_data))
    
    print("Data saved successfully to data/changi_jewel.txt")

if __name__ == "__main__":
    save_data()
