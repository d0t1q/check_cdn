IP Address CDN Checker
======================

This script is used to check a list of IP addresses and determine if they belong to known Content Delivery Networks (CDNs).

The script makes use of the `requests` and `json` libraries to send GET requests to the `http://rdap.arin.net/registry/ip/{IP}` URL, where `{IP}` is replaced with each IP address from a provided list. The script then checks the 'name' field in the returned JSON to find the Autonomous System Number (ASN) company name, which it then compares to a list of known CDN companies.

Dependencies
------------

*   Python 3.6+
*   `requests` library
*   `json` library

You can install these dependencies with `pip`:

`pip install requests`

IP List File Formatting
-----------------------

The IP addresses to be checked should be placed in a text file, with one IP address per line. For example:

`192.0.2.1 203.0.113.2 198.51.100.3`

No additional formatting is required. The script will read the file line by line and treat each line as a separate IP address to check.

Usage
-----

1.  Create a text file with the IP addresses to check, following the formatting guidelines outlined above.
2.  Run the script, passing the filename of the IP list as an argument:

bash

```bash
python3 cdn_check.py list.txt
```

If no file is provided, the script will display an error and ask for a file to be provided.

The script will read the IPs from the file, send a GET request to the `http://rdap.arin.net/registry/ip/{IP}` URL for each IP, and print out any IPs that are part of a known CDN.

The script includes a retry mechanism and a 0.5s wait time after each request to handle any errors and prevent overwhelming the server with too many requests in a short period of time.

Known CDN Companies
-------------------

The script currently checks for the following CDN companies:

*   Akamai
*   Amazon CloudFront
*   Cloudflare
*   Microsoft Azure
*   Google Cloud
*   AWS
*   Amazon
*   azure
*   microsoft
*   linode

You can add or remove CDN company names from the `CDNS` list in the script as needed.

Output
------

The script prints the progress of the IP checks in the console, and at the end it prints any IPs that were found to be part of a known CDN, along with the name of the CDN company. For example:

python

```python
Checking 50/100 IPs
...
Finished
172.105.253.139 is a part of the LINODE CDN
```

Error Handling
--------------

If an error occurs while checking an IP, the script will retry checking the IP up to 5 times before moving on to the next IP. The script also includes a 0.5s wait time after each request to prevent overwhelming the server with too many requests in a short period of time.

License
-------

This project is licensed under the terms of the MIT license.
