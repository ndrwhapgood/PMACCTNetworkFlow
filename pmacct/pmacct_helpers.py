import csv
import os
import subprocess
import netifaces
import time
import mysql.connector as mysql

#preserve order to keep things aligned with the database.
primitives = ['mac_src', 'mac_dst', 'vlan_in', 'ip_src', 'ip_dst', 'src_port', 'dst_port', 'ip_proto', 'packets', 'bytes', 'flows', 'class']
defaults = ['ip_src', 'ip_dst', 'src_port', 'dst_port', 'ip_proto']
friendlyName = {'ip_src': 'Source IP Address', 'ip_dst': 'Destination IP Address', 'src_port': 'Source Port', 'dst_port': 'Destination Port', 'ip_proto': 'Protocol'}

def GetColOptions():
    options = []
    for col in primitives:
        options.append(
            {'name': col, 
             'friendlyName': friendlyName.get(col) or col, 
             'checked': col in defaults
            })

    return options

def GetNetworkInterfaces():
    return netifaces.interfaces()

def IsPMACCTInstalled():
    # probably doens't need a script, clean up la
    return not subprocess.run(['bash', 'pmacct/check_install.sh'], capture_output=True, text=True) == ''

def InstallPMACCT():
    return subprocess.run(['bash', 'pmacct/install.sh'], capture_output=True, text=True)

def RunTestScript():
    return subprocess.run(['bash', 'pmacct/test.sh'], capture_output=True, text=True)

def StartDaemon(iface):
    print('staring daemon')

def ParseData(cols):
    total_data = []
    with open('pmacct/sample.csv', newline='') as sampleData:
        reader = csv.reader(sampleData, delimiter=' ')
        for row in reader:
            total_data.append(row)
    
    header = total_data[0][0].split(',')

    #get indexes for cols in header
    #TODO: put this in a try/catch block for if a column is not in the header.
    indexs = list(map(lambda c: header.index(c), cols))

    filtered_data = []
    for d in total_data:
        d = d[0].split(',')
        filtered_data.append([d[i] for i in indexs])

    return filtered_data

def Init():
    pmacct_db = mysql.connect(
        host='localhost',
        user='pmacct',
        password='arealsmartpwd',
        database='pmacct'
    )
    cursor = pmacct_db.cursor()
    cursor.execute('select * from acct limit 50')
    
    # prefetching data for testing.
    global data
    data = []
    for r in cursor:
        #print(r)
        data.append(r)

    return data

def GetData():
    return data

if __name__ == '__main__':
    print('testing...')
    #print(ParseData(['dst_ip', 'src_ip', 'proto']))
    #print(RunTestScript())
    #print(IsPMACCTInstalled())
    #print(GetNetworkInterfaces())
    #BuildConfFile('wlan', ['src_ip', 'dst_ip'], 'usefulename.csv')
    Init()
    print(GetData())