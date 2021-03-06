#        Read permissions:
#         - "e" = change directory (CWD command)
#         - "l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE, MDTM commands)
#         - "r" = retrieve file from the server (RETR command)
#
#        Write permissions:
#         - "a" = append data to an existing file (APPE command)
#         - "d" = delete file or directory (DELE, RMD commands)
#         - "f" = rename file or directory (RNFR, RNTO commands)
#         - "m" = create directory (MKD command)
#         - "w" = store a file to the server (STOR, STOU commands)
#         - "M" = change file mode (SITE CHMOD command)

import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler, ThrottledDTPHandler
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

resource_dir = ""
CERTFILE = os.path.abspath(os.path.join(os.path.dirname(__file__),"keycert.pem"))


class myHandler(TLS_FTPHandler):

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        os.remove(file)

def main():
    authorizer = DummyAuthorizer()
    #authorizer.add_user('user', '12345', '.', perm='elradfmwM')
    authorizer.add_user('user', '12345', '.', perm='elr')

    # cwd as home dir...should be resource dir later.
    authorizer.add_anonymous(os.getcwd())

    #dtp_handler = ThrottledDTPHandler
    #dtp_handler.read_limit = 1024000  # 1000 Kb/sec (1000 * 1024)
    #dtp_handler.write_limit = 1024000  # 1000 Kb/sec (1000 * 1024)

    #handler = FTPHandler
    #handler = TLS_FTPHandler
    handler = myHandler
    #handler.dtp_handler = dtp_handler
    handler.certfile = CERTFILE
    handler.tls_control_required = True
    handler.tls_data_required = True # too intensive .

    handler.authorizer = authorizer
    handler.timeout = 500 
    handler.max_login_attempts = 1
    handler.banner = "test"
    #handler.masquerade_address = '151.25.42.11'
    handler.passive_ports = range(60000, 60099)

    address = ("0.0.0.0",47274)
    #address = ("192.168.1.66",47274)
    server = FTPServer(address, handler)
    server.max_cons = 20
    server.max_cons_per_ip = 3
    server.serve_forever()


if __name__ == '__main__':
    main()
