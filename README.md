# caddy-to-mikrotik-static-dns

Add Locally hosted domains using Caddy to Mikrotik's static DNS

This script will scan all the domains hosted in your caddy server via caddy API, then add them as static DNS in a Mikrotik router using REST API.

## Prerequisites

1. Python3

## Connection details

You need the following in order to run the script successfully:

1. Caddy API URL. This is typically `localhost:2019`.
2. Mikrotik router access:
   1. Router URL (eg `192.168.1.1`)
   2. An user with write access. You'll need the username and password of the user

## Running the script

First download the `sync_dns.py` either by cloning this repo or downloading the zip.

There are 3 ways to run it:

### Interactive Shell (Easiest)

If you are going to run it once and forget about it then it's the easiest. Just run the script directly and it'll ask for all the details.

```bash
python sync_dns.py
```

You can skip IPv6 by entering blank.

### CLI Argument

You can run python `sync_dns.py -h` for help. An example command would be:

```bash
python sync_dns.py -c=localhost:2019 -m=192.168.1.1 -u=apiuser -p=supersecretpassword -i=192.168.1.2 -I=aa:bb:cc
```

You can skip the password and enter it in the interactive shell instead so it doesn't stay in your history or appear in the screen.

To skip ipv6, simply skip the `-I` or `--ipv6` flag.

### Configuration file

If you plan to run the scripts again and keeping the scripts in a single file Simply download the `config_sample.json` and rename it to `config.json`. Keep it in the same folder as `sync_dns.py`. Edit it as per your config. To skip IPv6, make its value to false. Once saved, run this command to load the config file:

```bash
python3 sync_dns.py -l
#or
python3 sync_dns.py --load-config
```

## TODO

I still have some improvements planned, but I'll probably never do it.

1. Make it so the script automatically runs when caddy restarts.
2. Package it and publish it somewhere, maybe in a PPA.
