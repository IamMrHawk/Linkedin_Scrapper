# Linkedin_Scrapper
LinkedIn Profile Scraper is a Python script that automates the process of logging into LinkedIn, searching for user profiles based on a specific keyword, and extracting desired data from those profiles. This README provides an overview of how to use and configure the script.

# Prerequisites
Before using this script, make sure you have the following dependencies installed:
- Python
- Selenium
- BeautifulSoup
- Chrome WebDriver
- A LinkedIn account

You can install Python packages using pip:
```console
pip install selenium beautifulsoup4
```

Download the Chrome WebDriver from the official website: ChromeDriver Downloads. Ensure it matches your installed Chrome version.

# Configuration
1. Create a config.json file in the same directory as the script. The file should have the following structure:

```console
{
  "search_query": "Python Developer",
  "username": "your_linkedin_username",
  "password": "your_linkedin_password",
  "chrome_driver_path": "path_to_chromedriver_executable",
  "num_profiles": 10,
  "out_data": {
    "name": true,
    "headline": true,
    "location": true,
    "current_company": true,
    "summary": true
  }
}
```

- 'search_query': The keyword you want to search for on LinkedIn.
- 'username': Your LinkedIn username.
- 'password': Your LinkedIn password.
- 'chrome_driver_path': The file path to your Chrome WebDriver executable.
- 'num_profiles': The number of profiles to scrape.
- 'out_data': Specify which profile data you want to extract (set to true to extract, false to skip).

# Usage
1. Make sure you have filled out the config.json file with your LinkedIn credentials and desired settings.

1. Run the script using Python:
```console
python linkedin_scraper.py
```

The script will log in to your LinkedIn account, perform the keyword search, and extract the specified data from user profiles. The results will be displayed in the terminal.

# Disclaimer
Please use this script responsibly and in compliance with LinkedIn's terms of service. Scraping LinkedIn profiles may be subject to legal restrictions, and it's essential to respect user privacy and data protection laws. Be aware that LinkedIn's policies can change, so ensure you are up-to-date with their current terms and conditions.
