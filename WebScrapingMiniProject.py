import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore

url = "https://quotes.toscrape.com"
username = "rootShree"
password = "1234"

def get_csrf_token(session, login_url):
    # To get the csrf_token
    # <input type="hidden" name="csrf_token" value="rSMsanLdRIqvFkEgBiAwNZbUlJOfeDyTzPYWHjphuVoKmGQxcCtX"/>
    resp = session.get(login_url)
    s = BeautifulSoup(resp.content, 'html.parser')

    input_tag = s.find('input', attrs = {'name': 'csrf_token'})

    if input_tag:
        return input_tag['value']
    else:
        print("[-] Couldn't find CSRF token!")
        return None

# get_csrf_token()

def login():
    session = requests.Session()

    login_url = f'{url}/login'

    token = get_csrf_token(session, login_url)

    if not token:
        session.close()
        return

    headers = {
        'Referer':login_url
    }

    data = {
        'csrf_token' : token,
        'username' : username,
        'password' : password
    }

    resp = session.post(login_url, data=data, headers=headers)

    if "Logout" in resp.text:
        print(f"[+] Login Successful as {username}")
    else:
        print("[-] Login Failed! The final response was: ")
        print(resp.text)

login()
