import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def web_scraper(url):
    try:
        # Send HTTP request
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()

        # Extract emails
        emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text_content)

        # Extract phone numbers (common formats)
        phone_regex = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
        phones = re.findall(phone_regex, text_content)

        # Extract website links
        links = [link.get('href') for link in soup.find_all('a') if link.get('href')]

        # Create DataFrame
        data = {
            'Website': [url],
            'Emails': [', '.join(set(emails))],
            'Phone Numbers': [', '.join(set(phones))],
            'Links': [', '.join(links)]
        }

        df = pd.DataFrame(data)
        return df

    except Exception as e:
        print(f"Error occurred: {e}")
        return pd.DataFrame()

# Main execution
if __name__ == "__main__":
    website_url = input("Enter website URL: ").strip()
    result_df = web_scraper(website_url)
    
    if not result_df.empty:
        # Save to CSV
        result_df.to_csv('website_data.csv', index=False)
        print("\nScraped Data:")
        print(result_df)
        print("\nData saved to website_data.csv")
    else:
        print("No data scraped or error occurred")