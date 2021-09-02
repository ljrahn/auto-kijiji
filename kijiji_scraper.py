import argparse
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from page_objects import HomePage, parse_page_item_links
import time


class Scraper:
    def __init__(self, options=None):
        self.chrome_options = Options()
        self.options = options

        if isinstance(options, list):
            for option in options:
                self.chrome_options.add_argument(f'--{option}')
            print(f'Using options {", ".join(options)} in chrome driver')
        elif isinstance(options, str):
            self.chrome_options.add_argument(f'--{options}')
            print(f'Using option {options} in chrome driver')
        elif options is None:
            print('Not using any chrome driver options')
        else:
            print('FATAL: specified incorrect options type')

    def start(self):
        
        if self.options is not None:
            self.driver = webdriver.Chrome(options=self.chrome_options)
        else:
            self.driver = webdriver.Chrome()

        self.home_page = HomePage(self.driver)

        start_url = "https://kijiji.ca"
        self.driver.get(start_url)
    
    def stop(self):
        self.driver.quit()

    def enter_input_data(self, product, location):
        self.product = product
        self.location = location
        self.home_page.product_search(product)
        self.home_page.select_location(location)
    
    def get_page_url(self):
        self.page_url = self.driver.current_url

    def get_all_ad_links(self):
        
        url = self.page_url.split('/')

        all_item_links = list()
        item_links_previous = list()
        same_page_flag = False
        for i in range(1, 10):
            local_url = url.copy()
            for idx, element in enumerate(url):
                if element.replace('-', ' ') == self.product:

                    local_url[idx] = element + f'/page-{i}'
                    local_url = '/'.join(local_url)

                    item_links_current = parse_page_item_links(local_url)
                    print(f'url: {local_url}')

                    if item_links_current == item_links_previous:
                        same_page_flag = True
                    else:
                        all_item_links.extend(item_links_current)
                        item_links_previous = item_links_current
                        
            if same_page_flag:
                break
        
        print(all_item_links)
        print(len(all_item_links))



        



if __name__ == '__main__':
    # scraper = Scraper(options='headless')
    scraper = Scraper()
    try:
        start_time = time.time()
        scraper.start()
        scraper.enter_input_data('macbook pro', 'New Dundee')
        scraper.get_page_url()
        scraper.stop()
        print(scraper.get_all_ad_links())
        print(time.time() - start_time)
    except Exception as e:
        print(f'{type(e).__name__}: {e}')
        scraper.stop()
    # scraper = Scraper()
    # scraper.product = 'macbook pro'
    # scraper.get_all_ad_links('https://www.kijiji.ca/b-kitchener-waterloo/macbook-pro/k0l1700212?rb=true&ll=43.349669%2C-80.533184&address=New+Dundee%2C+ON&radius=50.0&dc=true')

