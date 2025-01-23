import dns.resolver
import dns.reversename
import argparse
import ipaddress
import textwrap
from concurrent.futures import ThreadPoolExecutor

def print_banner(quiet):
    if quiet:
        return
    banner = textwrap.dedent(r"""
       ______                             ____  _   _______
      / ____/_  ___   ______  ____  _____/ __ \/ | / / ___/
     / / __/ / / / | / / __ \/ __ \/ ___/ / / /  |/ /\__ \ 
    / /_/ / /_/ /| |/ / / / / /_/ / /  / /_/ / /|  /___/ / 
    \____/\__,_/ |___/_/ /_/\____/_/  /_____/_/ |_//____/  

     Crafted by ello_guvnor

    """)
    print(banner)

def read_file(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            return [line.strip() for line in lines]
    except FileNotFoundError:
        print("File not found")
        return []
    except IOError as error:
        print(f"Error reading the file: {error}")
        return []

def write_file(filename, lines):
    with open(filename, "a") as file:
        for line in lines:
            file.write(f"{line}\n")

    print(f"The results have been successfully saved to {filename}") 

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def query_single_ptr(ip):
    try:
        reverse_name = dns.reversename.from_address(ip)
        ptr_record = dns.resolver.resolve(reverse_name, "PTR")
        return [rdata.to_text() for rdata in ptr_record]
    except Exception:
        return []

def query_ptr_multithread(ips, max_threads):
    futures = []
    results = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for ip in ips:
           futures.append(executor.submit(query_single_ptr,ip))
        
        for future in futures: 
            for result in future.result():
                results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(description="DNS request script with domain input.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--ip", type=str, help="The IP address to query")
    group.add_argument("-f", "--file", type=str, help="The file that contains IP addresses")

    parser.add_argument("-o", "--output", type=str, help="The file to save the output")
    parser.add_argument("--threads", type=int, default=10, help="The number of threads to use (default: 10)")
    parser.add_argument("--quiet", action="store_true", help="Do not show the banner or extra messages")
    
    args = parser.parse_args()

    print_banner(args.quiet)

    ptr_records = []
    max_threads = args.threads

    if max_threads <= 0: 
        print("Threads number must be greater than 0")
        return
    if max_threads > 100: 
        print("Threads number must be less than 100")
        return
    
    if args.ip:
        if validate_ip(args.ip):
            ptr_records = query_single_ptr(args.ip)
        else:
            print("Invalid IP address")
    elif args.file:
        ips = read_file(args.file)
        valid_ips = [ip for ip in ips if validate_ip(ip)]
        ptr_records = query_ptr_multithread(valid_ips, max_threads)
        
    
    for ptr_record in ptr_records:
        print(ptr_record)

    if args.output:
        write_file(args.output, ptr_records)

    

if __name__ == "__main__":
    main()

