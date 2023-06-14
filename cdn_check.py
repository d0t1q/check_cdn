import re
import requests
import sys
import json
import time
import argparse

# List of known CDN company names
CDNS = ['Akamai', 'Amazon CloudFront', 'Cloudflare', 'Google Cloud', 'AWS', 'Amazon', 'azure', 'microsoft', 'linode' ]

def read_ips_from_file(filename):
    """Read IP addresses from a file, remove '[.]' if it exists"""
    try:
        with open(filename, 'r') as file:
            # Substitute '[.]' with '.' in each line
            return [re.sub(r'\[\.\]', '.', line.strip()) for line in file]
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def lookup_asn_company(ip):
    """Look up the ASN company name for a given IP address"""
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(f"http://rdap.arin.net/registry/ip/{ip}")
            data = json.loads(response.text)
            return data.get('name')
        except Exception as e:
            print(f"Encountered an error checking {ip}, attempt {attempt}/{max_retries} to check again.")
            time.sleep(0.5)
            if attempt == max_retries:
                return None

def check_if_cdn(asn_company):
    """Check if the given ASN company name matches a known CDN"""
    if asn_company is not None:
        for cdn in CDNS:
            if cdn.lower() in asn_company.lower():
                return True
    return False

def main():
    """Main function to read IPs, check each one, and print CDN IPs"""
    parser = argparse.ArgumentParser(description='Check if IP addresses belong to known CDNs.')
    parser.add_argument('ip_list_file', type=str, help='The text file with the list of IP addresses to check.')
    args = parser.parse_args()

    # Read IPs from file
    ips = read_ips_from_file(args.ip_list_file)
    total_ips = len(ips)
    cdn_ips = []

    for i, ip in enumerate(ips, start=1):
        # Clear the line and print the current IP being checked
        sys.stdout.write('\r\033[K')
        sys.stdout.write(f'Checking {i}/{total_ips} IPs')
        sys.stdout.flush()

        # Lookup ASN and check if it's a CDN
        asn_company = lookup_asn_company(ip)
        if check_if_cdn(asn_company):
            cdn_ips.append((ip, asn_company))

        time.sleep(0.5)  # Sleep for 0.5s after each request

    # Print all CDN IPs after checking all IPs
    print("\nFinished")
    for ip, asn_company in cdn_ips:
        print(f'{ip} is a part of the {asn_company} CDN')

if __name__ == "__main__":
    main()
