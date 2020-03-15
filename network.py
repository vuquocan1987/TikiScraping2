import requests
from bs4 import BeautifulSoup
def get_soup(url):
    try:
        response = requests.get(url).text
        response = BeautifulSoup(response, 'html.parse')
        return response
    except Exception as err:
        print('Error on request:' , err)
