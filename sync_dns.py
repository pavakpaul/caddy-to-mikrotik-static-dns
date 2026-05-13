import os
import argparse
import requests
from sys import exit

def load_config_file():
    import json
    with open('config.json', 'r') as config_file:
        try:
            config = json.load(config_file)
            return (
                config["caddy_api_url"],
                config["mikrotik_url"],
                config["mikrotik_username"],
                config["mikrotik_password"]
            )
        except:
            print("Something went wrong with the config file, exiting")
            exit()

def prompt(q, sensitive=False):
    q = f"{q}: "
    if sensitive:
        import getpass
        a = getpass.getpass(q)
    else:
        a = input(q)
    return a

def parse_args_or_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--load-config", help="Load config.json file (no need for other arguments)", action='store_true')
    parser.add_argument("-c", "--caddy-url", help="Caddy API URL. Typically localhost:2019", nargs='?', const='localhost:2019')
    parser.add_argument("-m", "--mikrotik-url", help="Mikrotik router's URL")
    parser.add_argument("-u", "--mikrotik-user", help="Username for Mikrotik router")
    parser.add_argument("-p", "--mikrotik-pass", help="Username for Mikrotik router. Leave blank to use interactive shell to enter the password without printing in the shell")
    args = parser.parse_args()

    if args.load_config:
        caddy_url, mikrotik_url, mikrotik_user, mikrotik_pass = load_config_file()
    
    else:
        if args.caddy_url:
            caddy_url = args.caddy_url
        else:
            caddy_url = prompt("Enter the caddy API (typically localhost:2019)")
        if args.mikrotik_url:
            mikrotik_url = args.mikrotik_url
        else:
            mikrotik_url = prompt("Enter your Mikrotik router's URL")
        if args.mikrotik_user:
            mikrotik_user = args.mikrotik_user
        else:
            mikrotik_user = prompt("Enter the username for Mikrotik router")
        if args.mikrotik_pass:
            mikrotik_pass = args.mikrotik_pass
        else:
            mikrotik_pass = prompt("Enter the password for Mikrotik router", sensitive=True)
    
    return caddy_url, mikrotik_url, mikrotik_user, mikrotik_pass



def get_caddy_entries(url):
    if not url.startswith('http') and not url.startswith('https'):
        url = 'http://' + url
    url += '/config/apps/http/servers/srv0/routes/'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        print(data)
    else:
        print(f"Failed to get Caddy entries. Status code: {r.status_code}\nResponse: {r.text}")
        exit()




if __name__ == '__main__':
    caddy_url, mikrotik_url, mikrotik_user, mikrotik_pass = parse_args_or_input()

    get_caddy_entries(caddy_url)





