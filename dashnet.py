import logging
import json
import pprint
import requests

# Suppress InsecureRequestWarning: Unverified HTTPS request
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(filename='debug.log', level=logging.INFO)
config_file = open('./.config.json', "r")
config = json.load(config_file)
dashnet_token = config["dashnet_token"]



def get_data(element):
    req = "https://api.******************" + element
    #print(req)
    h = {'Accept': 'application/json', 'x-auth-token': dashnet_token}
    r = requests.get(req, verify=False, headers=h)
    data = r.text.replace(" ", "")
    data = data.replace("\\n", "")
    data = json.loads(data)
    #pprint.pprint(data)
    return data

def format_range(range):
    pattern = '/'
    replace = "%5C%2F"
    match = re.search(pattern, range)
    if match:
        return (re.sub(pattern, replace, range))
    else:
        print('pattern not found')



def copy_data():
    list = ['mag012', 'mag177', 'mag006', 'mag011', 'mag013', 'mag046', 'mag076', 'mag162', 'mag078', 'mag144',
            'mag154',
            'mag164', 'mag205', 'mag135']
    for element in list:
        ipam_data = get_data(element)
        for k,v in ipam_data.items():
                if 'networks' in v:
                    for network_info in v['networks']:
                        id_mag = network_info['site_id']
                        network_subnet = network_info['network']
                        vlan = network_info['vlan']
                        print(str(id_mag) +"--->" + str(network_subnet)+ "///" +str(vlan))
                        if vlan:
                            data = {}
                            new_entry = {'mag_id': id_mag, 'ip_range': network_subnet, 'vlan': vlan}
                            for key, value in new_entry.items():
                                data[key]=value
                                with open('data.json', 'a') as f:
                                    json.dump(data, f, indent=4)

copy_data()
