import requests
from bs4 import BeautifulSoup
import re

def parse_mac_addresses_and_dates(urls, output_file, success_file):
    with open(output_file, 'w', encoding='utf-8') as f, \
         open(success_file, 'a', encoding='utf-8') as success_f:  # Open success file in append mode

        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                mac_addresses = soup.find_all('code', string=re.compile(r'(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}'))

                if mac_addresses:  # Only write URL if MAC addresses are found
                    f.write(url + '\n')
                    success_f.write(url + '\n')  # Add to successful URLs list

                for mac_address_code in mac_addresses:
                    mac_address = mac_address_code.string.strip()

                    td = mac_address_code.find_parent('td')
                    if td:
                        url_element = td.find('a', href=True)
                        if url_element:
                            closest_url = url_element['href']
                            f.write(closest_url + '\n')

                    closest_date = None
                    for sibling in mac_address_code.next_siblings:
                        if isinstance(sibling, NavigableString):
                            date_match = re.search(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b', sibling)
                            if date_match:
                                closest_date = date_match.group(0)
                                break

                    if closest_date:
                        f.write(f"{mac_address} {closest_date}\n")
                    else:
                        f.write(mac_address + '\n')

                    f.write('\n')

            except requests.exceptions.RequestException as e:
                print(f"Error processing URL {url}: {e}")

if __name__ == '__main__':
    choice = input("Enter URLs directly (d) or from a file (f)? ")

    if choice.lower() == 'd':
        urls = input("Enter URLs separated by commas: ").split(',')
    elif choice.lower() == 'f':
        file_path = input("Enter the file path: ")
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f]
    else:
        print("Invalid choice. Exiting.")
        exit()

    output_file = 'extracted_data.txt'
    success_file = 'successful_urls.txt'  # File to store successful URLs
    parse_mac_addresses_and_dates(urls, output_file, success_file)
    print(f"Data has been written to {output_file}")