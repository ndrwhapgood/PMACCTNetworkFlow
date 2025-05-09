import csv
import os

columns = ['dst_ip', 'src_ip', 'dst_port', 'src_port', 'proto']
defaults = ['dst_ip', 'src_ip']
friendlyColumnName = {'dst_ip': 'Destiination Address', 'src_ip': 'Source Address'}

install_script = """echo 'testing'"""
pmacct_install_check = """echo 'checking for pmacct install' """

class ColOption:
    def __init__(self, name, friendlyName, isDefault):
        self.name = name
        self.friendlyName = friendlyName
        self.isChecked = isDefault

def GetColOptions():
    options = []
    for col in columns:
        options.append(ColOption(col, friendlyColumnName.get(col) or col, col in defaults))

    return options

def InstallPMACCT():
    os.system(install_script)
    return 0

def ParseData():
    return 0