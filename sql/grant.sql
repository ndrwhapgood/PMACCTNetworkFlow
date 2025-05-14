CREATE USER 'pmacct'@'localhost' IDENTIFIED BY 'arealsmartpwd';
GRANT ALL PRIVILEGES ON pmacct.* TO pmacct@localhost;

CREATE USER 'client'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON pmacct.* TO client@localhost;