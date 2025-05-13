drop database if exists pmacct;
create database pmacct;

use pmacct;

drop table if exists acct; 
create table acct (
    mac_src CHAR(17) NOT NULL,
    mac_dst CHAR(17) NOT NULL,
    vlan_in INT(2) UNSIGNED NOT NULL,
    ip_src CHAR(45) NOT NULL,
    ip_dst CHAR(45) NOT NULL,
    src_port INT(2) UNSIGNED NOT NULL,
    dst_port INT(2) UNSIGNED NOT NULL,
    ip_proto CHAR(6) NOT NULL, 
    packets INT UNSIGNED NOT NULL,
    bytes BIGINT UNSIGNED NOT NULL,
    flows INT UNSIGNED DEFAULT NULL,
    PRIMARY KEY (mac_src, mac_dst, vlan_in, ip_src, ip_dst, src_port, dst_port, ip_proto)
);