import requests
from bs4 import BeautifulSoup



radius = 56

website = f'https://www.kijiji.ca/b-woodstock-on/phone/k0l1700241?rb=true&woodstock%2C+ON+N4T+0J7%2C+canada&radius={radius}&dc=true'
page = requests.get(website)

soup = BeautifulSoup(page.text, 'html.parser')


entire_page = soup.find('body')

print(entire_page)


