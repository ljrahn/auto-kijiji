from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
start_url = "https://duckgo.com"
driver.get(start_url)
driver.quit()