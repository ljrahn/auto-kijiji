from utilities.selenium_functions import SeleniumUIActions
from bs4 import BeautifulSoup
import requests
import time


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.actions = SeleniumUIActions(driver)

        self.search_bar_id = 'SearchKeyword'
        self.location_select_id = 'SearchLocationPicker'
        self.location_search_id = 'SearchLocationSelector-input'
        self.location_first_element_xpath = '//*[@id="SearchLocationSelector-item-0" and not(contains(@class, "autocompleteSuggestion__currentLocation"))]'
        self.location_apply_xpath = '//*[contains(@class, "submitButton-2124651659 button-1997310527")]'
        
        # a href element for all items on a page
        self.all_items_links_xpath = '(//div[@class="info-container"]//div[@class="title"])'

        # pagination
        self.next_pages_xpath = '//div[@class="pagination"]'
        
    def product_search(self, keyword):
        self.actions.send_keys_element(locator='id', element=self.search_bar_id, keys=keyword)
    
    def select_location(self, location):
        self.actions.click_element(locator='id', element=self.location_select_id)
        self.actions.send_keys_element(locator='id', element=self.location_search_id, keys=location)
        self.actions.click_element(element=self.location_first_element_xpath)
        self.actions.click_element(element=self.location_apply_xpath)
    

def parse_page_item_links(url):
    full_html = requests.get(url)
    soup = BeautifulSoup(full_html.content, features="lxml")
    a_tags = soup.find_all('a', 'title')

    links = ['kijiji.ca' + a_tag.get('href') for a_tag in a_tags]
    return links

