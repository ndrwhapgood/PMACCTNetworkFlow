import subprocess

columns = ['dst_ip', 'src_ip', 'dst_port', 'src_port', 'proto']
defaults = ['dst_ip', 'src_ip']
friendlyColumnName = {'dst_ip': 'Destiination Address', 'src_ip': 'Source Address'}

class ColOption:
    def __init__(self, name, friendlyName, isDefault):
        self.name = name
        self.friendlyName = friendlyName
        self.isDefault = isDefault

def GetColOptions():
    options = []
    for col in columns:
        options.append(ColOption(col, friendlyColumnName.get(col) or col, col in defaults))

    return options

def InstallPMACCT():
    out = subprocess.run('/install.sh')
    return 0