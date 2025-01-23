# DNS PTR Query Script

This Python script allows you to query DNS PTR (reverse DNS) records for a single IP address or a list of IP addresses from a file. It supports multithreading to speed up querying multiple IP addresses and allows you to save the results to a file or display them in the terminal.

![Example](https://github.com/CandyCaneCapone/GuvnorDNS/blob/main/example.png?raw=true)

## Features

- Query a single IP address or multiple IP addresses from a file.
- Multithreaded PTR querying to speed up the process.
- Save PTR records to an output file.
- IP address validation to ensure only valid IPs are queried.


## Installation

To use the script, you will need to install the required dependencies. You can do this by running:

```bash
pip install -r requirements.txt
```

## Usage
```bash
python guvnordns.py -h
```

This will display help for you.
```Text
usage: guvnor_dns.py [-h] (-i IP | -f FILE) [-o OUTPUT] [--threads THREADS] [--quiet]

DNS request script with domain input.

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        The IP address to query
  -f FILE, --file FILE  The file that contains IP addresses
  -o OUTPUT, --output OUTPUT
                        The file to save the output
  --threads THREADS     The number of threads to use (default: 10)
  --quiet               Do not show the banner or extra messages

```
