import argparse
import json
import requests
from sys import exit

def load_config_file():
    with open('config.json', 'r') as config_file:
        # try:
            config = json.load(config_file)
            if not config["local_ipv6"]:
                config["local_ipv6"] = False
            return (
                config["caddy_api_url"],
                config["mikrotik_url"],
                config["mikrotik_username"],
                config["mikrotik_password"],
                config['local_ipv4'],
                config['local_ipv6']
            )
        # except:
        #     print("Something went wrong with the config file, exiting")
        #     exit()

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
    parser.add_argument("-i", "--ipv4", help="Enter the ipv4 address for localhost and 127.0.0.1")
    parser.add_argument("-I", "--ipv6", help="Enter the ipv6 address for localhost.")
    args = parser.parse_args()

    if args.load_config:
        caddy_url, mikrotik_url, mikrotik_user, mikrotik_pass, ipv4, ipv6 = load_config_file()
    
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
        if args.ipv4:
            ipv4 = args.ipv4
        else:
            ipv4 = prompt("Enter the IPv4 address of the server (where DNS should point to)")
        if args.ipv6:
            ipv6 = args.ipv6
        else:
            ipv6 = prompt("Enter the IPv4 address of the server (where DNS should point to for localhost.\nEnter blank to skip")
        if not ipv6 or ipv6 == 'blank':
            ipv6 = False

    return caddy_url, mikrotik_url, mikrotik_user, mikrotik_pass, ipv4, ipv6


def get_caddy_entries(url):
    if not url.startswith('http') and not url.startswith('https'):
        url = 'http://' + url
    url += '/config/apps/http/servers/srv0/routes/'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        caddy_entries = []
        for item in data:
            try:
                ip = item['handle'][0]['routes'][0]['handle'][0]['upstreams'][0]['dial']
                ip = ip.split(':')[0]
                domain = item['match'][0]['host'][0]

                print(f"Found {domain}  ---->  {ip}")
                caddy_entries.append((domain, ip))
            except:
                print(f"Skipping! Could not extract data for {item}")
        return caddy_entries
    else:
        print(f"Failed to get Caddy entries. Status code: {r.status_code}\nResponse: {r.text}")
        exit()

def get_mikrotik_records(url, user, passwd):
    url = url + '/rest/ip/dns/static/print'
    r = requests.post(url, auth=(user, passwd))
    if r.status_code == 200:
        data = r.json()
        records = []
        for record in data:
            domain = record['name']
            ip = record['address']
            dtype = record['type']
            records.append(
                {'name': domain, 'address': ip, 'type': dtype}
            )
        return records
    else:
        print(f"Failed to get static DNS records. Status code: {r.status_code}\nResponse: {r.text}")
        exit()

def add_mikrotik_record(url, user, passwd, record):
    url = url + '/rest/ip/dns/static/add'
    r = requests.post(url, auth=(user, passwd), data=json.dumps(record))
    if r.status_code == 200:
        return True
    else:
        print(f"Failed to add static DNS record. Status code: {r.status_code}\nResponse: {r.text}")
        exit()

if __name__ == '__main__':
    caddy_url, mikrotik_url, mikrotik_user, mikrotik_pass, ipv4, ipv6 = parse_args_or_input()
    print('Connecting to Caddy API to fetch hosted domains...')
    caddy_entries = get_caddy_entries(caddy_url)
    existing_names = []
    existing_records = get_mikrotik_records(mikrotik_url, mikrotik_user, mikrotik_pass)

    for record in existing_records:
        existing_names.append(record['name'])
    print(existing_names)

    for entry in caddy_entries:
        name = entry[0]
        if name in existing_names:
            print(f"{name} already exists in the DNS Records")
            continue
        address = entry[1]
        
        if address == '127.0.0.1' or address == 'localhost':
            add_mikrotik_record(mikrotik_url, mikrotik_user, mikrotik_pass, {
                'name': name,
                'address': ipv4,
                'type': 'A'
            })
            if ipv6:
                add_mikrotik_record(mikrotik_url, mikrotik_user, mikrotik_pass, {
                    'name': name,
                    'address': ipv6,
                    'type': 'AAAA'
            })
            print(f'Added {name}')
        else:
            add_mikrotik_record(mikrotik_url, mikrotik_user, mikrotik_pass, {
                'name': name,
                'address': address,
                'type': 'A'
            })
