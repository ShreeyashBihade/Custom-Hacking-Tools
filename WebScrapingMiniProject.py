import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore

url = "https://quotes.toscrape.com"

def get_csrf_token():
    # To get the csrf_token
    # <input type="hidden" name="csrf_token" value="rSMsanLdRIqvFkEgBiAwNZbUlJOfeDyTzPYWHjphuVoKmGQxcCtX"/>
    
    login_url = f'{url}/login'
    resp = requests.get(login_url)
    s = BeautifulSoup(resp.content, 'html.parser')

    input_tag = s.find('input', attrs = {'name': 'csrf_token'})

    if input_tag:
        token = input_tag['value']
        print(f'[+] The CSRF token is {token}')
    else:
        print("[-] Couldn't find CSRF token!")

get_csrf_token()
