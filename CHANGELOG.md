# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-14

### Added
- Initial release: `caddy-to-mikrotik-static-dns` sync utility
- Fetches hosted domains from Caddy server via REST API (`/config/apps/http/servers/srv0/routes/`)
- Creates static DNS entries on Mikrotik router via REST API (`/rest/ip/dns/static/`)
- Supports both `A` (IPv4) and `AAAA` (IPv6) DNS record types
- Three flexible input methods:
  - Interactive shell with masked password input (`getpass`)
  - Command-line arguments: `-c`, `-m`, `-u`, `-p`, `-i`, `-I`, `-l/--load-config`
  - JSON configuration file (`config.json`) for reusable setups
- Automatic substitution: when Caddy upstream is `localhost`/`127.0.0.1`, uses user-provided server IP instead
- IPv6 support is optional — skip by leaving input blank or setting `"local_ipv6": false`
- Clear console output showing discovered domains and sync progress
- Basic error handling with HTTP status feedback for API failures
- Documentation: `README.md` with prerequisites, usage examples, and configuration guide
- Sample config file (`config_sample.json`) for quick setup

### Security
- Passwords can be entered interactively without shell history exposure
- Config file support allows secure file permissions (`chmod 600 config.json`)

### Notes
- First public version — fully functional for local DNS sync workflows
- No external dependencies beyond Python 3 standard library + `requests`
