#!/usr/bin/env python3

import requests # type: ignore
import concurrent.futures
import sys
import warnings
import argparse
from colorama import init, Fore, Style # type: ignore
from urllib3.exceptions import InsecureRequestWarning # type: ignore

# Initialize colorama
init(autoreset=True)

# Suppress only the single InsecureRequestWarning from urllib3
warnings.simplefilter('ignore', InsecureRequestWarning)

banner = """
 ██████╗ ██╗████████╗               
██╔════╝ ██║╚══██╔══╝               
██║  ███╗██║   ██║                  
██║   ██║██║   ██║                  
╚██████╔╝██║   ██║                  
 ╚═════╝ ╚═╝   ╚═╝                  
                                    
 █████╗ ███╗   ██╗██████╗           
██╔══██╗████╗  ██║██╔══██╗          
███████║██╔██╗ ██║██║  ██║          
██╔══██║██║╚██╗██║██║  ██║          
██║  ██║██║ ╚████║██████╔╝          
╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝           
                                    
███╗   ███╗ ██████╗ ██████╗ ███████╗
████╗ ████║██╔═══██╗██╔══██╗██╔════╝
██╔████╔██║██║   ██║██████╔╝█████╗  
██║╚██╔╝██║██║   ██║██╔══██╗██╔══╝  
██║ ╚═╝ ██║╚██████╔╝██║  ██║███████╗
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
                                    
[@k2ito & @0xsn4k3000]
"""

# Print the banner
print(banner)

# List of paths to check
paths_to_check = [
    "/.git/HEAD",
    "/.git/config"
]

# Function to check a single URL
def check_url(url):
    results = []
    for path in paths_to_check:
        full_url = url.rstrip("/") + path
        try:
            response = requests.get(full_url, timeout=5, verify=False, allow_redirects=True)  # Allow redirects
            if response.history:
                last_response = response.history[-1]
            else:
                last_response = response
            if last_response.status_code == 200 and "[core]" in response.text:
                results.append(full_url)
        except (requests.Timeout, requests.ConnectionError):
            pass
    
    return results

# Function to process a single subdomain
def process_subdomain(subdomain):
    if not subdomain.startswith(('http://', 'https://')):
        url = f"https://{subdomain}"
    else:
        url = subdomain
    results = check_url(url)
    return results

# Main function to read subdomains and perform fuzzing
def main(subdomains_file, output_file, num_threads):
    with open(subdomains_file, "r") as file:
        subdomains = file.read().splitlines()

    accessible_git_files = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_subdomain = {executor.submit(process_subdomain, subdomain): subdomain for subdomain in subdomains}

        for future in concurrent.futures.as_completed(future_to_subdomain):
            subdomain = future_to_subdomain[future]
            try:
                result = future.result()
                if result:
                    accessible_git_files.extend(result)
                    print(Fore.GREEN + f"Subdomain: [+] {subdomain} has accessible .git files at {result}")
                else:
                    print(Fore.RED + f"Subdomain: [-] {subdomain} does not have accessible .git files.")
            except Exception as e:
                print(f"Error processing subdomain {subdomain}: {e}")

    # Save the results to the output file
    with open(output_file, "w") as f:
        for item in accessible_git_files:
            f.write("%s\n" % item)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fuzz subdomains for accessible .git files")
    parser.add_argument("-l", "--list", required=True, help="File containing list of subdomains")
    parser.add_argument("-o", "--output", default="accessible_git_files.txt", help="Output file to save accessible .git files (default: accessible_git_files.txt)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads to use (default: 10)")
    
    args = parser.parse_args()
    
    main(args.list, args.output, args.threads)
