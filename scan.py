import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys

def is_broken_link(url):
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code >= 400
    except requests.RequestException:
        return True

def scan_page_for_links(base_url):
    broken_links = []
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link_tag in soup.find_all('a', href=True):
            href = link_tag['href']
            full_url = urljoin(base_url, href)
            if urlparse(full_url).scheme in ['http', 'https']:
                if is_broken_link(full_url):
                    broken_links.append(full_url)
    except requests.RequestException as e:
        print(f"[ERROR] Could not retrieve {base_url}: {e}")
    return broken_links

def main(input_file, output_file):
    with open(input_file, 'r') as infile:
        urls = [line.strip() for line in infile if line.strip()]
    
    with open(output_file, 'w') as outfile:
        for url in urls:
            print(f"[INFO] Scanning: {url}")
            broken = scan_page_for_links(url)
            for b in broken:
                outfile.write(f"{url} -> Broken: {b}\n")
            print(f"[DONE] {len(broken)} broken links found on {url}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python broken_link_scanner.py <input_file.txt> <output_file.txt>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
