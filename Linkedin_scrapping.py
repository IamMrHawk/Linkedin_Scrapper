from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from contextlib import suppress
import json


class Linkedin_Scrapper:
    def __init__(self):
        self.options = None
        self.chromedriver_path = ''
        self.driver = None
        self.search_query = ''
        self.linkedin_username = ''
        self.linkedin_password = ''
        self.linkedin_url = 'https://www.linkedin.com/'
        self.num_profile = 0
        self.param_name = ''
        self.param_headline = ''
        self.param_location = ''
        self.param_current_company = ''
        self.param_summary = ''

        self.import_config()
        self.webdriver()
        self.login()
        self.keyword_search()
        self.extraction()
        self.driver.quit

    def import_config(self):
        with open('config.json') as config_file:
            data = json.load(config_file)
        config_file.close()
        self.search_query = data['search_query']
        self.linkedin_username = data['username']
        self.linkedin_password = data['password']
        self.chromedriver_path = data['chrome_driver_path']
        self.num_profile = data['num_profiles']
        self.param_name = data['out_data']['name']
        self.param_headline = data['out_data']['headline']
        self.param_location = data['out_data']['location']
        self.param_current_company = data['out_data']['current_company']
        self.param_summary = data['out_data']['summary']

    def webdriver(self):
        # creating WebDriver
        self.options = Options()
        self.options.add_argument("window-size=1200x600")
        self.driver = webdriver.Chrome(self.chromedriver_path, options=self.options)
        print('[+] Driver Created Successfully')

    def login(self):
        # Login to LinkedIn
        self.driver.get(self.linkedin_url)
        uname = self.driver.find_element(By.CSS_SELECTOR, 'label[for="session_key"]')
        passwd = self.driver.find_element(By.CSS_SELECTOR, 'label[for="session_password"]')

        username_input_id = uname.get_attribute('for')
        password_input_id = passwd.get_attribute('for')

        username_input = self.driver.find_element(By.ID, username_input_id)
        password_input = self.driver.find_element(By.ID, password_input_id)

        username_input.send_keys(self.linkedin_username)
        password_input.send_keys(self.linkedin_password)
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.driver.maximize_window()
        print('[+] Login Successful')

    def keyword_search(self):
        # Search for Keyword category
        search_input = self.driver.find_element(By.CSS_SELECTOR, 'input[role="combobox"]')
        search_input.send_keys(self.search_query)
        search_input.send_keys(Keys.RETURN)

        time.sleep(3)
        people = self.driver.find_element(By.XPATH, '//button[text()="People"]')
        people.click()

    def extraction(self):
        print('[+] Extracting Data')
        profiles = []
        time.sleep(3)
        search_results = self.driver.page_source
        soup = BeautifulSoup(search_results, 'html.parser')
        li_tags = soup.find_all('li', class_="reusable-search__result-container")[:self.num_profile]

        with suppress(Exception):
            for li in li_tags:
                # Finding <a> tag for href link
                link = li.find('a')
                if link:
                    href = link.get('href')
                    print(href)
                    # redirecting to user profile
                    self.driver.get(href)
                    # sleep till page get load
                    time.sleep(5)
                    # extracting page source info
                    source = self.driver.page_source
                    soup = BeautifulSoup(source, 'html.parser')

                    # Extracting particular type of Data
                    # Name
                    if self.param_name:
                        name = soup.find('div', class_='pv-text-details__title')
                        name = name.find('h1')
                        if name:
                            name = name.text

                    # HeadLine / Title
                    if self.param_headline:
                        Headline = soup.find('div', class_='text-body-medium break-words')
                        if Headline:
                            Headline = Headline.text.strip()

                    # Location
                    if self.param_location:
                        Location = soup.find('div', class_='pv-text-details__left-panel mt2')
                        Location = Location.find('span', class_='text-body-small inline t-black--light break-words')
                        if Location:
                            Location = Location.text.strip()

                    # Current Company
                    if self.param_current_company:
                        current_company = soup.find('div', id='experience', class_='pv-profile-card__anchor')
                        if current_company:
                            current_company = current_company.parent
                            if current_company:
                                current_company = current_company.find('li', class_='artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
                                if current_company:
                                    current_company = current_company.find('span', class_='t-14 t-normal')
                                    if current_company:
                                        current_company = current_company.find('span').text

                    # Summary / About
                    if self.param_summary:
                        summary = soup.find('div', class_='pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center')
                        if summary:
                            summary = summary.find('span')
                            summary = summary.text

                    profiles.append([name, Headline, Location, current_company, summary])
                    print(f'[+] Profile Data Fetched - {name}')

            for profile in profiles:
                print(profile, '\n\n')


if __name__ == '__main__':
    scrap = Linkedin_Scrapper()
