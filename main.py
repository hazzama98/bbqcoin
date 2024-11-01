import base64
import time 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests 
from urllib.parse import  parse_qs
import json 
import os
import pyfiglet
from colorama import Fore, Style, init
from user_agent import generate_user_agent


def encode_event(e, t):
    r = f"{e}|{t}|{int(time.time())}"
    n = "tttttttttttttttttttttttttttttttt"
    i = n[:16]
    key = n.encode('utf-8') 
    iv = i.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(r.encode('utf-8'), AES.block_size))
    return base64.b64encode(base64.b64encode(encrypted)).decode('utf-8')

init(autoreset=True)
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'access-control-allow-origin': '*',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'lan': 'en',
    'origin': 'https://bbqapp.bbqcoin.ai',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://bbqapp.bbqcoin.ai/',
    'sec-ch-ua': '"Android WebView";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent':'',
    'use-agen': '',
    'x-requested-with': 'org.telegram.messenger',
}

def key_bot():
    url = base64.b64decode("aHR0cDovL2l0YmFhcnRzLmNvbS9hcGkuanNvbg==").decode('utf-8')
    try:
        response = requests.get(url)
        response.raise_for_status()
        try:
            data = response.json()
            header = data['header']
            print(header)
        except json.JSONDecodeError:
            print(response.text)
    except requests.RequestException as e:
        print_(f"Failed to load header")
        
def bbq_tap(query_id ,taps):
    headers['user-agent'] = generate_user_agent('android')
    headers['use-agen'] = query_id
    id = str(json.loads(parse_qs(query_id)['user'][0])['id'])
    data = {
        'id_user':id,
        'mm': taps ,
        'game': encode_event(id,taps),
    }
    r = requests.post('https://bbqbackcs.bbqcoin.ai/api/coin/earnmoney', headers=headers, data=data)
    return (r.text)

def base_api():
    api = base64.b64decode("aHR0cHM6Ly9pdGJhYXJ0cy5jb20vYWlyZHJvcC9iYnFjb2luLmpzb24=").decode('utf-8')
    try:
        response = requests.get(api)
        response.raise_for_status()
        data = response.json()
        return data.get('api')
    except:
        exit()

def load_config():
    try:
        with open('config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        default_config = {
            "max_executions": 100,
            "cooldown_minutes": 30,
            "energy": 50000
        }
        with open('config.json', 'w') as file:
            json.dump(default_config, file, indent=4)
        return default_config

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
    config = load_config()
    energy = config['energy']
    max_executions = config['max_executions']
    cooldown_minutes = config['cooldown_minutes']
    
    base_api = base_api()
    if not base_api:
        print(Fore.RED + "Error: Failed to retrieve system API!")
        exit()
        
    max_attempts = 3
    for attempt in range(max_attempts):
        system_api = input(Fore.YELLOW + "Please enter system API: ")
        if system_api == base_api:
            break
        else:
            remaining = max_attempts - (attempt + 1)
            if remaining > 0:
                print(Fore.RED + f"Error: Invalid system API! Remaining attempts: {remaining}")
            else:
                print(Fore.RED + "Error: Maximum attempts exceeded!")
                exit()
    
    print(Fore.GREEN + "\nAuthentication successful!")
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    key_bot()

    print("\n\n")
    try:
        with open('query.txt', 'r') as file:
            queries = file.read().splitlines()
        
        if not queries:
            print(Fore.RED + "Error: Query file is empty!")
            exit()
            
    except FileNotFoundError:
        print(Fore.RED + "Error: Query file not found!")
        exit()
        
    success_counts = {query: 0 for query in queries}
    failed_counts = {query: 0 for query in queries}
    execution_count = 0
    
    lines_to_clear = len(queries) + 1
    
    while True:
        if execution_count >= max_executions:
            print(Fore.YELLOW + f"\nMaximum execution limit reached ({max_executions})")
            print(Fore.YELLOW + f"Waiting for cooldown period of {cooldown_minutes} minutes...")
            time.sleep(cooldown_minutes * 60)
            execution_count = 0
            print(Fore.GREEN + "\nResuming execution...")
        for query in queries:
            if query.strip():
                execution_count += 1
                user_data = json.loads(parse_qs(query)['user'][0])
                full_name = f"{user_data['first_name']}"
                
                print(f"\033[{lines_to_clear}A\033[J", end="")
                
                for q in queries:
                    ud = json.loads(parse_qs(q)['user'][0])
                    fn = f"{ud['first_name']}"
                    print(Fore.YELLOW + Style.BRIGHT + f"[⚔] ║ User: {fn} | Successful Operations: {success_counts[q]} | Failed Operations: {failed_counts[q]}")
                
                try:
                    data = bbq_tap(query, energy)
                    success_counts[query] += 1
                    print(Fore.GREEN + Style.BRIGHT + f"[⚔] ║ User: {full_name} | Coin injection completed successfully ♲")
                except:
                    failed_counts[query] += 1
                    print(Fore.RED + Style.BRIGHT + f"[⚔] ║ User: {full_name} | Coin injection operation failed ♲")
                
                time.sleep(0.1)
