import json
import logging
import urllib.parse
import ipaddress
import requests
# Suppress InsecureRequestWarning: Unverified HTTPS request
import urllib3
from dateutil.parser import parse
import netaddr
from netaddr import IPNetwork, IPAddress
from requests.auth import HTTPBasicAuth
import pprint
import re
from FlowTable import FlowTable
from db_conf import Session, engine, Base

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Base.metadata.create_all(engine)
MAXRESULTOMNILOG = 500000

# logging
logging.basicConfig(filename='debug.log', level=logging.INFO)
config_file = open('./.config.json', "r")
config = json.load(config_file)
graylog_username = config["graylog_username"]
graylog_password = config["graylog_password"]
dashnet_token = config["dashnet_token"]

# data
config_data_2 = open('data.json', "r")
result_file = json.load(config_data_2)


# Encodes query string
def encode_url(url):
    return urllib.parse.quote(url)

# Transforms entered European format date to American one + acceptable format for param_time in query
def format_param_time(start_date, end_date, start_time, end_time):
    result = start_date + 'T' + encode_url(
        start_time) + '.000Z&timerange-absolute-from=' + start_date + '%20' + encode_url(
        start_time) + '&to=' + end_date + 'T' + encode_url(
        end_time) + '.000Z&timerange-absolute-to=' + end_date + '%20' + encode_url(end_time)
    # result = start_date + 'T' + start_time + 'Z&timerange-absolute-to=' + end_date + 'T' + end_time + 'Z'
    return result


# Transforme la liste des mag pour la requête GET
def format_listmag():
    liste = ["((FR-LM_012_Lens%20node%201)", "(FR-LM_012_Lens%20node%202)", "(FR-LM_177_Annecy%20node%201)",
             "(FR-LM_177_Annecy%20node%202)", "(FR-LM_006_Nice%20node%201)", "(FR-LM_006_Nice%20node%202)",
             "(FR-LM_011_Villeneuve_d_Ascq%20node%201)", "(FR-LM_011_Villeneuve_d_Ascq%20node%202)",
             "(FR-LM_013_Montigny%20node%201)", "(FR-LM_013_Montigny%20node%202)", "(FR-LM_046_St_Brieuc%20node%201)",
             "(FR-LM_046_St_Brieuc%20node%202)", "(FR-LM_076_Marseille%20node%201)", "(FR-LM_076_Marseille%20node%202)",
             "(FR-LM_162_Besancon%20node%201)", "(FR-LM_162_Besancon%20node%202)", "(FR-LM_078_Compiegne%20node%201)",
             "(FR-LM_078_Compiegne%20node%202)", "(FR-LM_144_Reims_Nord%20node%201)",
             "(FR-LM_144_Reims_Nord%20node%202)", "(FR-LM_154_Annemasse%20node%201)",
             "(FR-LM_154_Annemasse%20node%202)",
             "(FR-LM_164_Verquin%20node%201)", "(FR-LM_164_Verquin%20node%202)",
             "(FR-LM_205_City_Batignolles%20node%201)", "(FR-LM_205_City_Batignolles%20node%202)",
             "(FR-LM_136_PFU_Gennevilliers%20node%201)", "(FR-LM_136_PFU_Gennevilliers%20node%202))"]
    result = "%20OR%20".join(liste)
    return result


# Transforme la liste des fields pour la requête GET
def format_listfields():
    liste_fields = ["source", "dstip", "comp_id", "srcip",
                    "vlansrc", "app", "protocol", "dstport", "state", "srcport"]
    result = ",".join(liste_fields)
    return result


def format_listvlan(num_vlan):
    liste = []
    for element in result_file:
        if num_vlan == 11:
            if element['vlan'] == '0011_Mgmt_AP':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 50:
            if element['vlan'] == '0050_Wifi':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 110:
            if element['vlan'] == '0110_UNIX':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 120:
            if element['vlan'] == '0120_ToIP':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 1:
            if element['vlan'] == '0001_Mgmt':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 130:
            if element['vlan'] == '0130_Devices':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 3012:
            if element['vlan'] == '3012_LMFRmobile_3012':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 9999:
            if element['vlan'] == '9999_NATed-IP':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 300:
            if element['vlan'] == '0300_DMZ1':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 302:
            if element['vlan'] == '0302_DMZ3':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 2:
            if element['vlan'] == '0002_Transit_FW':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 111:
            if element['vlan'] == '0111_Vegas':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 7:
            if element['vlan'] == '0007_Transit_Bouygues':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 8:
            if element['vlan'] == '0008_Transit_Bouygues2':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 5:
            if element['vlan'] == '0005_Transit_SFR':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
        if num_vlan == 6:
            if element['vlan'] == '0006_Transit_SFR2':
                value = element['ip_range_encoded']
                liste.append(value)
                result = "%20OR%20".join(liste)
    return result


def which_vlan(ip_destination):
    for element in result_file:
        if ipaddress.ip_address(ip_destination) in ipaddress.ip_network(element['ip_range']):
            return str([element["vlan"]])


# Gets logs
def get_logs(start_date, end_date, start_time, end_time, num_vlan):
    stream_id = "5cf62b2******"
    param_filter = "streams%3A" + stream_id
    param_time = format_param_time(start_date, end_date, start_time, end_time)
    liste_mag = "comp_id%3A" + format_listmag()
    liste_ip = "dstip%3A(" + format_listvlan(num_vlan) + ")"
    param_field = encode_url(format_listfields())
    param_query = liste_ip + "%20AND%20" + liste_mag
    url = "*************************************"
    req = url + param_query + "%20AND%20_exists_%3Astate" + "&from=" + param_time + "&limit=" + str(
        MAXRESULTOMNILOG) + "&filter=" + param_filter + "&fields=" + param_field + "&decorate=true"
    head = {'Accept': 'application/json'}
    r = requests.get(req, verify=False, auth=HTTPBasicAuth(graylog_username, graylog_password), headers=head)
    data = r.text.replace(" ", "")
    data = data.replace("\\n", "")
    data = json.loads(data)
    return data


def run_app(start_date, end_date, start_time, end_time,num_vlan):
    session = Session()
    i = 0
    while i < 1:
        loglist = get_logs(start_date, end_date, start_time, end_time,num_vlan)
        if "messages" in loglist.keys():
            for logmessage in loglist["messages"]:
                log = logmessage["message"]
                ip_source = log.get("srcip")
                firewall_node_ip = log.get("source")
                ip_destination = log.get("dstip")
                vlan_destination = which_vlan(ip_destination)
                firewall_node = log.get("comp_id")
                application = log.get("app")
                protocol = log.get("protocol")
                vlan_source = log.get("vlansrc")
                destination_port = log.get("dstport")
                source_port = log.get("srcport")
                state = log.get("state")
                timestamp = log.get("timestamp")
                print(str(application) + " - " + str(firewall_node) + " --> " + str(
                    ip_destination) + " : " + "vlansrc:" + str(
                    vlan_source) + " : " + str(destination_port) + "/" + str(protocol) + str(timestamp))
                is_in_db = session.query(FlowTable).filter(FlowTable.ip_source == ip_source) \
                    .filter(FlowTable.ip_destination == ip_destination) \
                    .filter(FlowTable.firewall_node_ip == firewall_node_ip) \
                    .filter(FlowTable.protocol == protocol) \
                    .filter(FlowTable.firewall_node == firewall_node) \
                    .filter(FlowTable.source_port == source_port) \
                    .filter(FlowTable.state == state) \
                    .filter(FlowTable.destination_port == destination_port) \
                    .filter(FlowTable.application == application) \
                    .filter(FlowTable.vlan_source == vlan_source) \
                    .filter(FlowTable.vlan_destination == vlan_destination).count()
                # print(is_in_db)
                if is_in_db == 0:
                    to_add = FlowTable(vlan_source, ip_source, firewall_node, firewall_node_ip, ip_destination,
                                       protocol,
                                       state,
                                       application, source_port, destination_port, vlan_destination)
                    session.add(to_add)
                    session.commit()
                    print("New Flow added in DB")
                else:
                    print("Skipped:Already in DB")
        i = i + 1
    session.close()


run_app('2020-10-03', '2020-10-05', '00:07:00', '00:00:00', 50)
