#!/usr/bin/env python
# coding: utf-8

# Import required libraries
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import csv

# Define a regex pattern to extract dates
dateRegex = re.compile(r"\w{3}\s\d{2}\,\s\d{4}")

# Initialize a dictionary to store news and dates
df = {"News": [], "Date": []}

# Define the URL to scrape
link = "https://timesofindia.indiatimes.com/topic/kerala/news"

# Send a GET request to the URL
r1 = requests.get(link)

# Save the content of the page
coverpage = r1.content

# Parse the content using BeautifulSoup
soup1 = BeautifulSoup(coverpage, "html.parser")

# Loop through all news items
for news in soup1.find_all('div', {"class": "Mc7GB"}):
    # Extract the date using regex
    dateresult = dateRegex.search(news.text).group()
    
    # Format the date
    dateFormatted = datetime.strptime(dateresult, "%b %d, %Y").date()
    
    # Append news and date to the dictionary
    df["News"].append(news.text.strip())
    df["Date"].append(dateFormatted)

# Save the data to a CSV file
csv_file = "news_data.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(["News", "Date"])
    
    # Write the data
    for news, date in zip(df["News"], df["Date"]):
        writer.writerow([news, date])

print(f"Data saved to {csv_file}")