#!/usr/bin/python

import sys
import requests

# disable warnings from SSL Check
if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")

req = requests.get('https://172.168.10.150', verify=False)

print(req)
