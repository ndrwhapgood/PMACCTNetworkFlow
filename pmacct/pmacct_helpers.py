import csv
import os
import subprocess

columns = ['dst_ip', 'src_ip', 'dst_port', 'src_port', 'proto']
defaults = ['dst_ip', 'src_ip', 'dst_port', 'src_port', 'proto']
friendlyColumnName = {'dst_ip': 'Destiination Address', 'src_ip': 'Source Address'}

def GetColOptions():
    options = []
    for col in columns:
        options.append(
            {'name': col, 
             'friendlyName': friendlyColumnName.get(col) or col, 
             'checked': col in defaults
            })

    return options

def InstallPMACCT():
    return subprocess.run(['bash', 'pmacct/install.sh'], capture_output=True, text=True)

def RunTestScript():
    return subprocess.run(['bash', 'pmacct/test.sh'], capture_output=True, text=True)

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

if __name__ == '__main__':
    print('testing...')
    #print(ParseData(['dst_ip', 'src_ip', 'proto']))
    print(RunTestScript())