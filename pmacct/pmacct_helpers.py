import csv
import os
import subprocess
from subprocess import call
import netifaces
import mysql.connector as mysql
from datetime import date

#preserve order to keep things aligned with the database.
primitives = ['mac_src', 'mac_dst', 'vlan_in', 'ip_src', 'ip_dst', 'src_port', 'dst_port', 'ip_proto', 'packets', 'bytes', 'flows', 'class']
defaults = ['ip_src', 'ip_dst', 'src_port', 'dst_port', 'ip_proto' ,'packets', 'bytes', 'class']
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
    # probably doens't need a script, clean up later
    return not subprocess.run(['bash', 'pmacct/check_install.sh'], capture_output=True, text=True) == ''

def InstallPMACCT():
    return subprocess.run(['bash', 'pmacct/install.sh'], capture_output=True, text=True)

def RunTestScript():
    return subprocess.run(['bash', 'pmacct/test.sh'], capture_output=True, text=True)

def BuildConfig(iface):
    iface_key = 'pcap_interface'
    with open('pmacct/pmacct.conf', 'r') as confFile:
        lines = confFile.readlines()

    with open('pmacct/pmacct.conf', 'w') as confFile:
        for line in lines:
            if line.startswith(iface_key):
                iface_key_value = iface_key + ': ' + iface
                confFile.write(iface_key_value)
            else:
                confFile.write(line)

def StartDaemon(iface):
    print(f'starting daemon on {iface}')
    BuildConfig(iface)
    call('sudo pmacctd -f pmacct/pmacct.conf -F tmp.txt', shell=True)    

def KillDaemon():
    with open('tmp.txt', 'r') as name:
        pmacct_pid = name.read()
    call(f'sudo kill -9 {pmacct_pid}', shell=True)
    print('daemon slain')
    os.remove('tmp.txt')


def Init():
    global pmacct_db # global to keep the db connection persistant.
    pmacct_db = mysql.connect(
        host='localhost',
        user='pmacct',
        password='arealsmartpwd',
        database='pmacct'
    )
    # refresh since daemon will write to the db regardless of interface.
    ClearData()

def GetData():
    cursor = pmacct_db.cursor()
    cursor.execute('select * from acct orlimit 100')
    data = []
    for row in cursor:
        data.append(row)

    return data

def GetDisplayData(limit):
    cursor = pmacct_db.cursor()
    sql_cmd = f'select {", ".join(primitives)} from acct order by updated_time limit {limit};'
    cursor.execute(sql_cmd)
    data = []
    for row in cursor:
        data.append(row)
    return data

def ClearData():
    # clear db when we change interface
    cursor = pmacct_db.cursor()
    cursor.execute('truncate table acct')

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

    # calculate clever file name
    cleverName = FindCleverFileName(indexes)
    fileName = dir + '/' + cleverName + '.csv'
    header = [primitives[i] for i in indexes]
    table = GetData()
    data = []
    for row in table:
        d = [row[i] for i in indexes]
        data.append(d)

    with open(fileName, 'w') as newFile:
        writer = csv.writer(newFile)
        writer.writerow(header)
        writer.writerows(data)

    print('done')

def FindFunFacts():
    # get stuff like, what src address has sent the most data
    # typical bytes per packet
    # most common class
    return []

if __name__ == '__main__':
    print('testing...')
    #print(RunTestScript())
    #print(IsPMACCTInstalled())
    #print(GetNetworkInterfaces())
    #BuildConfFile('wlan', ['src_ip', 'dst_ip'], 'usefulename.csv')
    #Init()
    #ClearData()
    #print(GetData())
    #SaveData([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    #StartDaemon('wlp6s0')