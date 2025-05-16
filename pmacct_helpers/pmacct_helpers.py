import csv
import os
import subprocess
from subprocess import call
import netifaces
import mysql.connector as mysql
from datetime import date
import time

#preserve order to keep things aligned with the database.
primitives = ['mac_src', 'mac_dst', 'vlan_in', 'ip_src', 'ip_dst', 'src_port', 'dst_port', 'ip_proto', 'packets', 'bytes', 'flows', 'class']
defaults = ['ip_src', 'ip_dst', 'src_port', 'dst_port', 'ip_proto' ,'packets', 'bytes', 'class']
friendlyName = {'ip_src': 'Source IP Address', 'ip_dst': 'Destination IP Address', 'src_port': 'Source Port', 'dst_port': 'Destination Port', 'ip_proto': 'Protocol'}

clr_cmd = 'TRUNCATE TABLE acct'

seed_cmd = """
INSERT INTO acct (mac_src, mac_dst, vlan_in, ip_src, ip_dst, src_port, dst_port, ip_proto, packets, bytes, flows, class)
VALUES
('00:1A:2B:3C:4D:5E', '00:1A:2B:3C:4D:5E', '0', '10.0.0.1', '10.0.0.1', '0', '0', 'tcp', '1', '1', '0', 'unknown/someguy'),
('01:1A:2B:3C:4D:5E', '01:1A:2B:3C:4D:5E', '0', '10.0.0.2', '10.0.0.2', '0', '0', 'tcp', '1', '1', '0', 'unknown/someguy'),
('02:1A:2B:3C:4D:5E', '02:1A:2B:3C:4D:5E', '0', '10.0.0.3', '10.0.0.3', '0', '0', 'tcp', '1', '1', '0', 'unknown/someguy'),
('03:1A:2B:3C:4D:5E', '03:1A:2B:3C:4D:5E', '0', '10.0.0.4', '10.0.0.4', '0', '0', 'tcp', '1', '1', '0', 'unknown/someguy'),
('04:1A:2B:3C:4D:5E', '04:1A:2B:3C:4D:5E', '0', '10.0.0.5', '10.0.0.5', '0', '0', 'tcp', '1', '1', '0', 'unknown/someguy');
"""

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

def InstallPMACCT():
    return subprocess.run(['bash', 'pmacct_helpers/install.sh'], capture_output=True, text=True)

def BuildConfig(iface):
    iface_key = 'pcap_interface'
    with open('pmacct_helpers/pmacct.conf', 'r') as confFile:
        lines = confFile.readlines()

    with open('pmacct_helpers/pmacct.conf', 'w') as confFile:
        for line in lines:
            if line.startswith(iface_key):
                iface_key_value = iface_key + ': ' + iface
                confFile.write(iface_key_value)
            else:
                confFile.write(line)

def StartDaemon(iface):
    print(f'summoning daemon on {iface}')
    BuildConfig(iface)
    call('sudo pmacctd -f pmacct_helpers/pmacct.conf -F tmp.txt', shell=True)    

def KillDaemon():
    call('sudo kill -9 $(sudo cat tmp.txt)', shell=True)
    print('daemon slain')
    os.remove('tmp.txt')


def Init():
    pmacct_db = mysql.connect(
        host='localhost',
        user='client',
        password='password',
        database='pmacct'
    )

    cursor = pmacct_db.cursor()
    cursor.execute(clr_cmd)

    cursor.close()
    pmacct_db.close()

def SeedDatabase():
    pmacct_db = mysql.connect(
        host='localhost',
        user='client',
        password='password',
        database='pmacct'
    )

    cursor = pmacct_db.cursor()
    cursor.execute(seed_cmd)

    cursor.close()
    pmacct_db.commit()
    pmacct_db.close()

def GetData(limit):
    pmacct_db = mysql.connect(
        host='localhost',
        user='client',
        password='password',
        database='pmacct'
    )

    cursor = pmacct_db.cursor()
    cmd = f'SELECT {", ".join(primitives)} FROM acct ORDER BY updated_time DESC LIMIT {limit};'
    cursor.execute(cmd)

    d = []
    for row in cursor:
        d.append(row)
    global data # set global data here to sync ui with backend
    data = d

    cursor.close()
    pmacct_db.close()

    return data

def GetDataV2(limit, filters={}):
    # this opens up more possibilities for sql injection bugs but not my problem.
    # placeholder till testing is complete.
    if len(filters) == 0:
        return GetData(limit)
    
    pmacct_db = mysql.connect(
        host='localhost',
        user='client',
        password='password',
        database='pmacct'
    )

    cursor = pmacct_db.cursor()

    # filter <column name>: <str>
    # basic filter for now, we just do a check if that column contians that str
    _f = []
    for key in filters:
        _f.append(f' {key} LIKE \'%{filters[key]}%\'')
    
    where_statements = []
    for i in _f:
        where_statements.append(i)
        where_statements.append('AND')

    cmd = f'SELECT {", ".join(primitives)} FROM acct WHERE {" ".join(where_statements).strip('AND ')} LIMIT {limit}'
    cursor.execute(cmd)

    d = []
    for row in cursor:
        d.append(row)
    global data
    data = d
    
    cursor.close()
    pmacct_db.close()

    return data
    

def GetCurrentDataContext():
    return data

def FindCleverFileName(indexes):
    # not so clever way to finding names
    if len(indexes) == len(primitives):
        return 'kitchen_sink'
    # if all indexes are in the defaults
    # return default
    elif indexes == [3, 4]:
        return 'essentials'
    elif len(indexes) == 1:
        return 'why'
    elif indexes == [11]:
        return 'okay'
    # concat primitive names?
    return 'foobar'

def SaveData(indexes):
    dir = date.today().isoformat()
    if not os.path.exists(dir):
        os.makedirs(dir)

    cleverName = FindCleverFileName(indexes)
    fileName = dir + '/' + cleverName + '.csv'
    header = [primitives[i] for i in indexes]
    table = GetCurrentDataContext()
    data = []
    for row in table:
        d = [row[i] for i in indexes]
        data.append(d)

    with open(fileName, 'w') as newFile:
        writer = csv.writer(newFile)
        writer.writerow(header)
        writer.writerows(data)

def CalculateBytes():
    current_data = GetCurrentDataContext()
    total_bytes = 0
    for d in current_data:
        total_bytes = total_bytes + d[9]
    
    i = 0
    scale = ['', 'K', 'M', 'G']    # if you need more than this you have a problem
    while int(total_bytes / 1000) > 1 and (i < len(scale) -1):
        total_bytes = int(total_bytes / 1000)
        i = i + 1

    return f'You have transfed {total_bytes} {scale[i]}B of data.'

def FindMostCommonClass():
    if len(data) == 0:
        return ''
    
    counts = {}
    for d in data:
        key = d[11].split('/')[1] # expected <name>/<name>
        # ignore unknowns
        if not key == 'Unknown':
            if not key in counts:
                counts[key] = 1
            else:
                counts[key] = counts[key] + 1
    largest_key = max(counts, key=counts.get)
    return f'You have interacted with {largest_key} {counts[largest_key]} times.'

def GetFunFacts():
    # possible optimizations would be do to the calculations through sql.
    facts = []
    facts.append(CalculateBytes())
    facts.append(FindMostCommonClass())

    return facts

if __name__ == '__main__':
    print('testing...')
    # GetData(41)
    # print(CalculateBytes())
    # print(FindMostCommonClass())
    #GetDataV2(100, {'class': 'youtube', 'src_port': '0'})
    #Init()
    SeedDatabase()