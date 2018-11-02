import requests
import jsbeautifier
import sys

# disable warnings from SSL Check
if not sys.warnoptions:
    import warnings

warnings.simplefilter("ignore")

# POST BODY
creds = ('administrator@vsphere.local', 'VxR@il1!')
runtype = {"dryrun": "false"}  # if true only does pre-checks
headers = {'Content-type': 'application/json'}

shut_resp = requests.post('https://172.168.10.150/rest/vxm/v1/cluster/shutdown',
                          verify=False,
                          headers=headers,
                          auth=creds,
                          json=runtype)

shut__resp_code = shut_resp.status_code

# assign a dict type to the response
job_id = shut_resp.json()

req_id = job_id.get('request_id')

print(f'''
#######################
# API CALL SUBMITTED  #
#######################

Shutdown Cluster API Submitted. Response Code is: {shut__resp_code} and request_id is: {req_id}

''')

# we check now the request status from previous call

resp_get_id = requests.request('GET', 'https://172.168.10.150/rest/vxm/v1/requests/' + req_id,
                               verify=False,
                               auth=creds)

beauty = jsbeautifier.beautify(resp_get_id.text)

print('''
##################################
# The Status of the API CALL is: #
##################################

''', beauty)
