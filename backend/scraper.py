import requests
from bs4 import BeautifulSoup
import csv
import time
import random

def scrape_ikman_iphones(target_count=3000):
    base_url = "https://ikman.lk"
    # The URL structure must place the page number correctly to be recognized
    search_url_template = "https://ikman.lk/en/ads/sri-lanka/mobile-phones?sort=date&order=desc&buy_now=0&urgent=0&page={}&enum.os=ios"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    scraped_data = []
    page = 1
    
    # Define the fields for the CSV
    fieldnames = ["Price", "Condition", "Brand", "Model", "Edition", "Operating System", 
                  "RAM", "Memory", "No. of Camera", "Screen Size", "Network", 
                  "SIM Support", "Dual SIM", "URL"]

    # Open file in write mode to start fresh
    with open('ikman_iphones_full.csv', 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        while len(scraped_data) < target_count:
            current_search_url = search_url_template.format(page)
            print(f"--- Scraping Listing Page: {page} ---")
            
            try:
                # 1. Fetch the listing page
                response = requests.get(current_search_url, headers=headers, timeout=15)
                if response.status_code != 200:
                    print(f"Error: Server returned status {response.status_code}. Breaking.")
                    break

                soup = BeautifulSoup(response.text, 'html.parser')
                listings = soup.find_all('a', class_='card-link--3ssYv gtm-ad-item')
                
                if not listings:
                    print("No more listings found on this page. Stopping.")
                    break

                for list_item in listings:
                    if len(scraped_data) >= target_count:
                        break
                        
                    ad_url = base_url + list_item['href']
                    
                    try:
                        # 2. Fetch the individual detail page
                        ad_response = requests.get(ad_url, headers=headers, timeout=15)
                        ad_soup = BeautifulSoup(ad_response.text, 'html.parser')
                        
                        # Extract Price
                        price_div = ad_soup.find('div', class_='amount--3NTpl')
                        price = price_div.text.strip() if price_div else ""

                        # Extract Specifications from the grid
                        details = {}
                        meta_rows = ad_soup.find_all('div', class_='full-width--XovDn')
                        for row in meta_rows:
                            label_div = row.find('div', class_='label--3oVZK')
                            value_div = row.find('div', class_='value--1lKHt')
                            if label_div and value_div:
                                key = label_div.text.replace(':', '').strip()
                                details[key] = value_div.text.strip()

                        # Construct row data
                        row_data = {
                            "Price": price,
                            "Condition": details.get("Condition", ""),
                            "Brand": details.get("Brand", ""),
                            "Model": details.get("Model", ""),
                            "Edition": details.get("Edition", ""),
                            "Operating System": details.get("Operating System", ""),
                            "RAM": details.get("RAM", ""),
                            "Memory": details.get("Memory", ""),
                            "No. of Camera": details.get("No. of Camera", ""),
                            "Screen Size": details.get("Screen Size", ""),
                            "Network": details.get("Network", ""),
                            "SIM Support": details.get("SIM Support", ""),
                            "Dual SIM": details.get("Dual SIM", ""),
                            "URL": ad_url
                        }
                        
                        # Save immediately to CSV
                        writer.writerow(row_data)
                        scraped_data.append(row_data)
                        print(f"Collected ({len(scraped_data)}/{target_count}): {row_data['Model']}")
                        
                        # Human-like delay between detail pages
                        time.sleep(random.uniform(1.0, 2.5)) 

                    except Exception as e:
                        print(f"Error scraping detail page {ad_url}: {e}")
                        continue

                # Increment page number for the next loop iteration
                page += 1 
                # Slightly longer delay after finishing a full search page
                time.sleep(3)

            except requests.exceptions.RequestException as e:
                print(f"Connection error: {e}. Waiting 10s before retry...")
                time.sleep(10)

    print(f"Scraping finished. Total records: {len(scraped_data)}")

if __name__ == "__main__":
    scrape_ikman_iphones(3000)