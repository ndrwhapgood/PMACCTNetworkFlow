import csv
import os
import subprocess

primitives = [ 'src_mac', 'dst_mac', 'vlan', 'in_vlan', 'out_vlan', 'in_cvlan', 'out_cvlan', 'cos', 'etype',
            'src_host', 'dst_host', 'src_net', 'dst_net', 'src_mask', 'dst_mask', 'src_as', 'dst_as',
            'src_port', 'dst_port', 'tos', 'proto', 'none', 'sum_mac', 'sum_host', 'sum_net', 'sum_as',
            'sum_port', 'flows', 'flow_label', 'tag', 'tag2', 'label', 'class', 'tcpflags', 'in_iface',
            'out_iface', 'std_comm', 'ext_comm', 'lrg_comm', 'as_path', 'peer_src_ip', 'peer_dst_ip',
            'peer_src_as', 'peer_dst_as', 'local_pref', 'med', 'dst_roa', 'src_std_comm',
            'src_ext_comm', 'src_lrg_comm', 'src_as_path', 'src_local_pref', 'src_med', 'src_roa',
            'mpls_vpn_rd', 'mpls_pw_id', 'mpls_label_top', 'mpls_label_bottom', 'mpls_label_stack',
            'sampling_rate', 'sampling_direction', 'src_host_country', 'dst_host_country',
            'src_host_pocode', 'dst_host_pocode', 'src_host_coords', 'dst_host_coords',
            'nat_event', 'fw_event', 'post_nat_src_host', 'post_nat_dst_host', 'post_nat_src_port',
            'post_nat_dst_port', 'tunnel_src_mac', 'tunnel_dst_mac', 'tunnel_src_host',
            'tunnel_dst_host', 'tunnel_proto', 'tunnel_tos', 'tunnel_src_port', 'tunnel_dst_port',
            'tunnel_tcpflags', 'tunnel_flow_label', 'fwd_status', 'vxlan', 'nvgre', 'timestamp_start',
            'timestamp_end', 'timestamp_arrival', 'timestamp_export', 'export_proto_seqno',
            'export_proto_version', 'export_proto_sysid', 'path_delay_avg_usec',
            'path_delay_min_usec', 'path_delay_max_usec', 'srv6_seg_ipv6_list', 'vrf_name' ]
defaults = ['dst_host', 'src_host', 'dst_port', 'src_port', 'proto']
friendlyName = {'dst_host': 'Destiination Address', 'src_host': 'Source Address'}

def GetColOptions():
    options = []
    for col in primitives:
        options.append(
            {'name': col, 
             'friendlyName': friendlyName.get(col) or col, 
             'checked': col in defaults
            })

    return options

def IsPMACCTInstalled():
    # probably doens't need a script, clean up la
    return not subprocess.run(['bash', 'pmacct/check_install.sh'], capture_output=True, text=True) == ''

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
    #print(RunTestScript())
    #print(IsPMACCTInstalled())